from django.contrib import admin
from .models import Sport, EquipmentType, Equipment

# Rekisteröidään Sport ja EquipmentType Django Admin -paneeliin
admin.site.register(Sport)
admin.site.register(EquipmentType)
admin.site.register(Equipment)
