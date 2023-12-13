from django import forms
from .models import Country,NumberPeople,Category

class CountryForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Country.objects.all(),label='Выберите страну вашего отеля')

class PeopleNumberForm(forms.Form):
    number = forms.ModelChoiceField(queryset=NumberPeople.objects.all(),label='Выберите количество людей',required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория",required=False)

class DateForm(forms.Form):
    start_date = forms.DateField(
        label='Выберите дату заезда',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='Выберите дату выезда',
        widget=forms.DateInput(attrs={'type': 'date'})
    )