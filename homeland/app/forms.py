from django import forms
from .models import Country,NumberPeople

class CountryForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Country.objects.all())

class PeopleNumberForm(forms.Form):
    number = forms.ModelChoiceField(queryset=NumberPeople.objects.all())



