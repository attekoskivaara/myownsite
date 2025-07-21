from django.contrib import admin

# Register your models here.

from django.contrib import admin
from activities_app.models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('type', 'user', 'start_date')
