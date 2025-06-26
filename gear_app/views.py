from django.shortcuts import render, redirect, get_object_or_404
from .models import Gear, EquipmentType, Sport, Equipment
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from activities_app.models import Activity
from django.http import JsonResponse
from .forms import GearForm, EquipmentForm
from django.contrib import messages
from gear_app.gear_custom_fields import GEAR_CUSTOM_FIELDS
import pandas as pd

def gear_dashboard(request):
    return render(request, "gear_app/gear_dashboard.html")

@login_required
def equipment_submit(request):
    if request.method == 'POST':
        sport_id = request.POST.get('sport')
        equipment_type_id = request.POST.get('equipment_type')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        size = request.POST.get('size')
        weight = request.POST.get('weight')
        purchase_date = request.POST.get('purchase_date')
        purchase_price = request.POST.get('purchase_price')
        default_use_ids = request.POST.getlist('default_uses') # Tämä tulee lomakkeelta ID:nä
        status = request.POST.get('status')


        # Käsitellään custom_fields
        custom_fields = {}
        for key, value in request.POST.items():
            if key.startswith('custom_fields['):
                field_name = key[len('custom_fields['):-1]  # Hae kentän nimi (esim. "Shoe Size")
                custom_fields[field_name] = value

        # Hae sport- ja equipment_type -objektit
        sport = Sport.objects.get(id=sport_id)
        equipment_type = EquipmentType.objects.get(id=equipment_type_id)
        #default_use_sport = Sport.objects.get(id=default_use_id) # Muutettu: haetaan Sport-instanssi

        # Luo Equipmenupt-objekti
        equipment = Equipment.objects.create(
            user=request.user,  # Ensure this is set
            sport=sport,
            equipment_type=equipment_type,
            brand=brand,
            model=model,
            size=size,
            weight=weight or None,  # Jätä tyhjä, jos arvoa ei annettu
            purchase_date=purchase_date or None,
            purchase_price=purchase_price or None,
            custom_fields=custom_fields,  # Tallenna JSON-muotoiset dynaamiset kentät
       #     default_uses=default_use_sport,
            status=status,
        )

        # Lisää default_uses monivalintana
        if default_use_ids:
            for sport_id in default_use_ids:
                sport_obj = Sport.objects.get(id=sport_id)
                equipment.default_uses.add(sport_obj)

        return redirect('gear_list')  # Ohjaa onnistuneen tallennuksen jälkeen

    return redirect('equipment_form')  # Ohjaa takaisin lomakkeelle, jos ei POST-py


def equipment_form_view(request):
    sports = Sport.objects.all()  # Haetaan kaikki lajit
    return render(request, 'gear_app/equipment_form.html', {'sports': sports})


def get_equipment_types(request):
    sport_id = request.GET.get('sport_id')
    print("TROLOL")
    equipment_types = EquipmentType.objects.filter(sport_id=sport_id)
    print(equipment_types)
    data = [
        {
            'id': et.id,
            'name': et.name,
            'custom_field_structure': et.custom_field_structure
        } for et in equipment_types
    ]
    return JsonResponse(data, safe=False)



def get_equipment_fields(request):
    equipment_type_id = request.GET.get("equipment_type_id")
    equipment_type = EquipmentType.objects.filter(id=equipment_type_id).first()

    if equipment_type and equipment_type.custom_fields:
        return JsonResponse({"custom_fields": equipment_type.custom_fields})
    else:
        return JsonResponse({"custom_fields": []})


@login_required
def my_gear_view(request):
    print(f"Current User: {request.user}")  # Debugging line
    '''
    related_activities = Activity.objects.filter(gears=self)
    print(f"Related activities for equipment {self}: {related_activities}")

    for activity in related_activities:
        print(f"Activity ID: {activity.id}, Duration: {activity.duration}")
    '''
    gear_data = Equipment.objects.filter(user=request.user).select_related('sport', 'equipment_type')
    return render(request, 'gear_app/gear_list.html', {'gear_data': gear_data})


@login_required
def gear_add_view(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.user = request.user
            equipment.save()
            form.save_m2m()  # tärkeä ManyToMany-kentille kuten default_uses
            return redirect('gear_list')
    else:
        form = EquipmentForm()

    return render(request, 'gear_app/gear_add.html', {'form': form})

# tästä egear edit..
@login_required
def equipment_edit(request, equipment_id):
    gear = get_object_or_404(Equipment, id=equipment_id, user=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=gear)
        if form.is_valid():
            form.save()
            return redirect('gear_list')  # tai minne haluat
    else:
        form = EquipmentForm(instance=gear)

    return render(request, 'gear_app/equipment_edit.html', {'form': form, 'gear': gear})


@login_required
def gear_edit_view(request, pk):
    sports = Sport.objects.all()  # Haetaan kaikki lajit
    gear = get_object_or_404(Equipment, pk=pk)
    custom_fields_structure = GEAR_CUSTOM_FIELDS.get(gear.equipment_type.name, [])
    print("POST default_uses:", request.POST.getlist('default_uses'))

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=gear)

        # Custom field data extraction
        custom_fields = gear.custom_fields or {}
        for key, value in request.POST.items():
            if key.startswith('custom_fields['):
                field_name = key.split('custom_fields[')[-1].rstrip(']')
                custom_fields[field_name] = value
        if form.is_valid():
            gear = form.save(commit=False)
            gear.custom_fields = custom_fields
            gear.save()
            form.save_m2m()
            messages.success(request, 'Gear updated successfully!')

            return redirect('gear_list')
    else:
        form = EquipmentForm(instance=gear)

    return render(request, 'gear_app/gear_edit.html', {
        'form': form,
        'gear': gear,
        'custom_fields_structure': custom_fields_structure,
        'sports': sports,
    })


@login_required
def equipment_delete(request, gear_id):
    gear = get_object_or_404(Equipment, id=gear_id, user=request.user)
    if request.method == "POST":
        gear.delete()
        return redirect('gear_list')  # tai minne haluat ohjata poistamisen jälkeen

def get_custom_fields(request, equipment_type_id):
    try:
        equipment_type = EquipmentType.objects.get(pk=equipment_type_id)
        custom_fields = equipment_type.custom_fields  # Oletetaan, että custom_fields on JSON
        return JsonResponse(custom_fields)
    except EquipmentType.DoesNotExist:
        return JsonResponse({'error': 'Equipment type not found'}, status=404)