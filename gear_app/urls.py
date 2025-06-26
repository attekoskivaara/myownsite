from django.urls import path, include
from . import views
from .views import gear_edit_view, get_custom_fields, equipment_form_view, get_equipment_types, equipment_submit
from django.contrib import admin
import gear_app.dash_apps.gear_dash  # Tämä tarvitaan! Pakottaa rekisteröinnin


urlpatterns = [
  #  path('gears/', views.gear_list_view, name='gear_list'),
    path('gears/add/', views.gear_add_view, name='gear_add'),
    path('gears/edit/<int:pk>/', views.gear_edit_view, name='gear_edit'),
  #  path('gears/delete/<int:gear_id>/', views.gear_delete_view, name='gear_delete'),
    path('equipment/<int:gear_id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('gear_list/', views.my_gear_view, name='gear_list'),
    path('equipment_form/', equipment_form_view, name='equipment_form'),
    path('equipment_submit/', equipment_submit, name='equipment_submit'),
    path('get-equipment-types/', views.get_equipment_types, name='get_equipment_types'),    path('get_equipment_fields/', views.get_equipment_fields, name='get_equipment_fields'),
    path('equipment/submit/', views.equipment_submit, name='equipment_submit'),
    path('get_custom_fields/<int:equipment_type_id>/', get_custom_fields, name='get_custom_fields'),
    #path('gear/update/<int:gear_id>/', views.gear_update_view, name='gear_update'),
    path('equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('gear/edit/<int:pk>/', gear_edit_view, name='gear_edit'),
    path("gear_dashboard/", views.gear_dashboard, name="gear_dashboard"),

]

