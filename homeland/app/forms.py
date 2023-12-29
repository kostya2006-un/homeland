from django import forms
from .models import Country, NumberPeople, Category, Review, HotelRating


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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        labels = {'text': 'Текст отзыва'}
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class HotelRatingForm(forms.ModelForm):
    class Meta:
        model = HotelRating
        fields = ['rating']
