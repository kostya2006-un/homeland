from django import forms
from .models import Country

class CountryForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Country.objects.all())



