from django import forms
from .models import Sport, EquipmentType, Equipment, Gear


class EquipmentForm(forms.ModelForm):
    sport = forms.ModelChoiceField(queryset=Sport.objects.all(), label="Sport")
    equipment_type = forms.ModelChoiceField(queryset=EquipmentType.objects.all(), label="Equipment Type")

    class Meta:
        model = Equipment
        fields = ['sport', 'equipment_type', 'brand', 'model', 'purchase_date', 'purchase_price', 'default_uses', 'status']

        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'default_uses': forms.CheckboxSelectMultiple,
        }


# uuden gearin lisäys form
class GearForm(forms.ModelForm):
    class Meta:
        model = Gear
        fields = ['name', 'gear_type', 'purchase_date', 'purchase_price', 'retailer',
                  'maintenance_log', 'estimated_lifespan_km', 'weight', 'manufacturer']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),  # This adds a date picker
        }

    def __init__(self, *args, **kwargs):
        super(GearForm, self).__init__(*args, **kwargs)
        # This ensures the correct date format
        self.fields['purchase_date'].input_formats = ['%Y-%m-%d']
