from django import forms
from .models import Country,NumberPeople,Order

class CountryForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Country.objects.all())

class PeopleNumberForm(forms.Form):
    number = forms.ModelChoiceField(queryset=NumberPeople.objects.all())

class DateForm(forms.Form):
    start_date = forms.DateField(
        label='Выберите дату заезда',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='Выберите дату выезда',
        widget=forms.DateInput(attrs={'type': 'date'})
    )