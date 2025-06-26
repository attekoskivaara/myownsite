# activities/forms.py
from django import forms
from .models import Activity
from gear_app.models import Equipment


class GearSelectForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['gears']  # Assuming "gears" is a ManyToManyField in Activity model
        widgets = {
            'gears': forms.CheckboxSelectMultiple(),  # Display gears as checkboxes
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Poimitaan käyttäjä argumenteista
        super().__init__(*args, **kwargs)
        if user:
            # Suodatetaan 'gears' vain kirjautuneen käyttäjän lisäämiin välineisiin
            self.fields['gears'].queryset = Equipment.objects.filter(user=user).order_by('sport')

        else:
            # Tyhjä queryset, jos käyttäjää ei anneta
            self.fields['gears'].queryset = Equipment.objects.none()