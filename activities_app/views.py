import certifi
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import Activity
from gear_app.models import Equipment
from user_app .models import UserProfile
from django.contrib import messages
from social_django.models import UserSocialAuth
from datetime import datetime, timedelta
from .forms import GearSelectForm
import datetime
from django.utils.timezone import now
from django.db import IntegrityError
from django.utils import timezone
from gear_app.models import Sport
import re


# Replace these with your actual Strava client details
STRAVA_CLIENT_ID = '112240'
STRAVA_CLIENT_SECRET = 'a47dc730e03f40df1950a5d2ab8e0a91fe7d7a1b'
STRAVA_REDIRECT_URI = 'http://localhost:8000/activities/strava_callback_view/'


@login_required
def view_activities(request):
    # Check if the user has synced activities
    user_activities = Activity.objects.filter(user=request.user).order_by('-start_date')
    print("HEADERIT")
    df = pd.DataFrame.from_records(user_activities.values())
    print(df)

    # Tulosta ensimmäinen rivi

    # Hae kaikki käyttäjän välineet
    user_gears = Equipment.objects.filter(user=request.user)
    print(user_activities)
    activity_gears = {
        activity.id: list(activity.gears.values_list('id', flat=True))
        for activity in user_activities
    }
    print("Activity gears:", activity_gears)
    if user_activities.exists():
        # If activities exist, pass them to the template
        return render(request, 'activities_app/activities_list.html', {
            'activities': user_activities,
            'user_gears': user_gears,
            'activity_gears': activity_gears,
        })
    else:
        # If no activities found, show a sync button
        return render(request, 'activities_app/no_activities.html')


@login_required
def sync_strava(request):
    """Sync Strava activities and store them in the local database."""
    access_token = request.session.get('strava_access_token')

    if not access_token:
        return redirect('strava_auth')  # Redirect to Strava login if token is missing

    strava_activities = fetch_strava_activities(access_token)

    # Only save new activities (not already in the database)
    for activity_data in strava_activities:
        strava_id = activity_data['id']

        if not Activity.objects.filter(strava_id=strava_id, user=request.user).exists():
            # Create and save a new Activity object
            # Muunna Strava API:n antamat sekunnit timedelta-muotoon
            duration_in_seconds = activity_data['elapsed_time']  # Tämä on kesto sekunteina
            duration = datetime.timedelta(seconds=duration_in_seconds)  # Muutetaan timedelta-muotoon

            moving_time_in_seconds = activity_data['moving_time']
            moving_time = datetime.timedelta(seconds=moving_time_in_seconds)

            # Muunna distance metreistä kilometreiksi
            distance_in_km = activity_data['distance'] / 1000
            Activity.objects.create(
                user=request.user,
                strava_id=strava_id,
                type=activity_data['type'],
                name=activity_data['name'],
                distance=distance_in_km,
                duration=duration,
           #     type=activity_data['type'],
                start_date=activity_data['start_date'],
                elevation_gain=activity_data['total_elevation_gain'],
                average_speed=activity_data['average_speed'],
                average_heartrate=activity_data['average_heartrate'],
                moving_time=moving_time
             #   average_speed=activity_data['average_speed'],
            )

    return redirect('activities_list')


# Synkronointifunktio

def activity_edit(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    sports = Sport.objects.all()

    if request.method == 'POST':
        sport_id = request.POST.get('sport_type')
        sport = get_object_or_404(Sport, id=sport_id)
        activity.sport_type = sport.name

        activity.start_date = request.POST.get('start_date')

        # Parse duration as hh:mm:ss
        duration_str = request.POST.get('duration')
        try:
            h, m, s = map(int, duration_str.split(':'))
            activity.duration = timedelta(hours=h, minutes=m, seconds=s)
        except:
            activity.duration = timedelta(0)  # fallback if parsing fails

        # parse moving time as hh:mm:ss
        moving_time_str = request.POST.get('moving_time')
        try:
            h, m, s = map(int, moving_time_str.split(':'))
            activity.moving_time = timedelta(hours=h, minutes=m, seconds=s)
        except:
            activity.moving_time = timedelta()


        activity.distance = request.POST.get('distance') or 0
        activity.elevation_gain = request.POST.get('elevation_gain') or 0

        activity.save()
        return redirect('activities_list')

    return render(request, 'activities_app/activity_edit.html', {
        'activity': activity,
        'sports': sports,
    })


def split_camel_case(name):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)


def sync_strava_activities(request):
    # Get user's access token (assuming you store it in UserProfile)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Muuta access_tokenin vanhenemisaika awareksi, jos se on naive

    # User has never synced
    if not user_profile.strava_refresh_token:
        return strava_auth_view(user_profile)

    if user_profile.strava_token_expires_at:
        if timezone.is_naive(user_profile.strava_token_expires_at):
            user_profile.strava_token_expires_at = timezone.make_aware(user_profile.strava_token_expires_at)

    # Tarkista, onko access_token vanhentunut
    if user_profile.strava_token_expires_at is None or user_profile.strava_token_expires_at < timezone.now():
        print("Access token has expired, refreshing...")
        refresh_strava_token(user_profile)
    #    if not token_refreshed:
    #        return render(request, 'error.html', {'message': 'Access tokenin päivittäminen epäonnistui.'})


    # Synkronointitoimet
    access_token = user_profile.strava_access_token
    strava_activities = fetch_strava_activities(access_token)  # Tämä kutsuu Strava APIa
    new_activities = 0

    existing_strava_ids = set(Activity.objects.filter(user=request.user).values_list('strava_id', flat=True))

    if strava_activities:
        # Haetaan jo tietokannassa olevien aktiviteettien Strava ID:t
        #existing_strava_ids = set(Activity.objects.filter(user=request.user).values_list('strava_id', flat=True))

        for activity_data in strava_activities:
            activity_id = activity_data['id']
            moving_time_seconds = activity_data['moving_time']
            moving_time = datetime.timedelta(seconds=moving_time_seconds)
            duration_in_seconds = activity_data['elapsed_time']  # Tämä on kesto sekunteina
            duration = datetime.timedelta(seconds=duration_in_seconds)  # Muutetaan timedelta-muotoon

            distance_in_km = activity_data['distance'] / 1000

            strava_sport_type = activity_data.get('sport_type', '')
            formatted_sport_type = split_camel_case(strava_sport_type)

            start_date = timezone.make_aware(datetime.datetime.strptime(activity_data['start_date'], '%Y-%m-%dT%H:%M:%SZ')),
            # start_date_str = activity_data['start_date']
            # start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%SZ')

            # Tarkistetaan, onko aktiviteetti jo kannassa
            if activity_id not in existing_strava_ids:
                # Jos ei ole, yritetään luoda uusi aktiviteetti

                # Tarkista ja muunna 'start_date' vain, jos se on merkkijono
                start_date = activity_data.get('start_date')
                if isinstance(start_date, str):
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
                    start_date = timezone.make_aware(start_date)


                sport_type_name = activity_data.get('sport_type')
                print(sport_type_name)
                sport = Sport.objects.filter(name__iexact=sport_type_name).first()

                if sport:
                    default_gear = Equipment.objects.filter(user=request.user, default_uses=sport).first()
                else:
                    default_gear = None

                new_activity = Activity.objects.create(
                        strava_id=activity_id,
                        name=activity_data['name'],
                        distance=distance_in_km,
                        duration=duration,
                        moving_time=moving_time,
                        start_date=start_date,
                        elevation_gain=activity_data['total_elevation_gain'],
                        # Suoraan tässä
                        #sport_type pitäisi olla esim. "trail run"
                        sport_type=formatted_sport_type,
                        # type pitäisi kääntää "trail run" -> "run"
                        type=activity_data['type'],
                        user=request.user
                    )
                if default_gear:
                    new_activity.gears.add(default_gear)

                new_activities += 1

        # Päivitetään viimeisin synkronointiaika
        user_profile.last_synced = now()
        user_profile.save()
    messages.success(request, f"{new_activities} new activities added.")
    return redirect('activities_list')


def seconds_to_hms(seconds):
    return str(datetime.timedelta(seconds=seconds))


# Step 5: Display synced activities in a dashboard
@login_required
def activities_dashboard(request):
    """Show all synced activities in the dashboard."""
    activities = Activity.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'activities_list.html', {'activities': activities})


# Funktio hakee Strava-aktiviteetit ja palauttaa ne
def fetch_strava_activities(access_token):
    print("entä täällä :D:D:D:D")
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    # Tulosta vastauskoodi ja -sisältö debuggausta varten
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code == 200:
        print("toimii")
        return response.json()
    else:
        print("ei toimi")
        return None


def refresh_strava_token(user_profile):
    url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': STRAVA_CLIENT_ID,  # Korvaa omalla client_id:lläsi
        'client_secret': STRAVA_CLIENT_SECRET,  # Korvaa omalla client_secret:lläsi
        'refresh_token': user_profile.strava_refresh_token,
        'grant_type': 'refresh_token',
    }
    response = requests.post(url, data=payload, verify=certifi.where())
    response_data = response.json()

    if response.status_code == 200:
        print("tämä1")
        # Päivitä käyttäjän access token ja refresh token
        user_profile.strava_access_token = response_data['access_token']
        user_profile.strava_refresh_token = response_data['refresh_token']
        user_profile.strava_token_expires_at = datetime.datetime.utcfromtimestamp(response_data['expires_at'])
        user_profile.save()

        return True

    else:
        print("tämä2")
        print(f"Failed to refresh token: {response_data}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response_data}")

        # Check for invalid refresh token error
        if response_data.get('errors') and response_data['errors'][0]['code'] == 'invalid':
            print("Invalid refresh token, redirecting to authorization page...")
            authorization_url = f"https://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&redirect_uri={STRAVA_REDIRECT_URI}&response_type=code&scope=activity:read_all"
            print(authorization_url)
            print("JOO?!")
            return redirect(authorization_url)

        return False

def exchange_code_for_tokens(auth_code):
    print("Käykö täällä? :D")
    url = 'https://www.strava.com/oauth/token'

    payload = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'code': auth_code,
        'grant_type': 'authorization_code',
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    return response_data


def save_strava_activities(user):
    print("2")
    # Fetch activities from Strava API
    activities = fetch_strava_activities(user)
    if activities:
        for activity_data in activities:
            strava_id = activity_data['id']
            # Check if the activity with this strava_id already exists
            if not Activity.objects.filter(strava_id=strava_id).exists():
                print(f"Saving new activity with ID: {strava_id}")

                # Muunna Strava API:n antamat sekunnit timedelta-muotoon
                duration_in_seconds = activity_data['elapsed_time']  # Tämä on kesto sekunteina
                duration = datetime(seconds=duration_in_seconds)  # Muutetaan timedelta-muotoon

                # Create a new Activity instance and save it
                activity = Activity(
                    user=user,
                    strava_id=activity_data['id'],
                    name=activity_data['name'],
                    distance=activity_data['distance'] / 1000,  # Convert meters to kilometers
                    duration=duration,  # Duration in seconds
                    sport_type=activity_data['sport_type'],
                    start_date=activity_data['start_date'],
                    average_speed=activity_data['average_speed'],
                    average_heartrate=activity_data['average_heartrate']
                )
                try:
                    activity.save()
                    print(f"Successfully saved activity with ID: {strava_id}")
                except Exception as e:
                    print(f"Error saving activity with ID: {strava_id}: {e}")
            else:
                print(f"Activity with ID {strava_id} already exists in the database. Skipping save.")
    else:
        print("No activities to save.")
    print(activities)


@login_required
def strava_auth_view(request):
    """Redirect the user to Strava's authorization page."""
    auth_url = (
        f"https://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code&redirect_uri={STRAVA_REDIRECT_URI}"
        f"&approval_prompt=force&scope=read,activity:read_all"
    )
    return redirect(auth_url)


@login_required
# Handle Strava's callback after the user authorizes your app

def strava_callback_view(request):
    auth_code = request.GET.get('code')
    print("päästiinkö tänne")
    if auth_code:
        token_data = exchange_code_for_tokens(auth_code)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.strava_access_token = token_data['access_token']
        user_profile.strava_refresh_token = token_data['refresh_token']
        user_profile.strava_token_expires_at = datetime.datetime.utcfromtimestamp(token_data['expires_at'])
        user_profile.save()
        return redirect('activities_list')
    else:
        return render(request, 'error.html', {'message': 'Authorization failed.'})


@login_required
def activity_list_view(request):
    """Display the user's Strava activities in a Pandas DataFrame."""
    access_token = request.session.get('strava_access_token')
    if not access_token:
        return redirect('strava_auth_view')

    # Fetch the user's activities from Strava's API
    response = requests.get(
        'https://www.strava.com/api/v3/athlete/activities',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    if response.status_code == 200:
        activities = response.json()

        # Create a Pandas DataFrame from the activities
        df = pd.DataFrame(activities)

        # Select columns to display in the DataFrame
        df = df[['sport_type', 'distance', 'moving_time', 'type', 'start_date']]

        # Convert 'moving_time' from seconds to H:M:S format using pandas to_timedelta
        df['moving_time'] = pd.to_timedelta(df['moving_time'], unit='s')

        # Format moving_time without displaying days (just H:M:S)
        df['moving_time'] = df['moving_time'].apply(lambda x: str(x).split('days')[-1].strip())
        print("HEADERIT")
        print(df.columns.tolist())
        # Convert DataFrame to HTML (without index)
        activities_html = df.to_html(classes='table table-striped', index=False)

        # Pass the HTML to the template context
        return render(request, 'activities_app/activities_list.html', {'activities_html': activities_html})
    else:
        return render(request, 'activities_app/activities_list.html', {'error': 'Failed to fetch activities from Strava'})




@login_required
def assign_gear(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == 'POST':
        form = GearSelectForm(request.POST, instance=activity, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('activities_list')

    else:
        form = GearSelectForm(instance=activity, user=request.user)

    return render(request, 'activities_app/assign_gear.html', {'form': form})