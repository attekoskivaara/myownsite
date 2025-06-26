from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_activities, name='activities_list'),
    path('strava_auth/', views.strava_auth_view, name='strava_auth'),
    path('strava_callback_view/', views.strava_callback_view, name='strava_callback_view'),
    path('sync-strava/', views.sync_strava, name='sync_strava'),
    path('fetch_activities/', views.fetch_strava_activities, name='fetch_activities'),
    path('save_activities/', views.save_strava_activities, name='save_activities'),
    path('activities/assign_gear/<int:activity_id>/', views.assign_gear, name='assign_gear'),
    path('sync_strava_activities/', views.sync_strava_activities, name='sync_strava_activities'),
    path('activities/<int:activity_id>/edit/', views.activity_edit, name='activity_edit'),

]

