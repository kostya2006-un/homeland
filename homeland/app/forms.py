from django import forms
from .models import Country, NumberPeople, Category, Review, HotelRating
from django.utils.safestring import mark_safe

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
class StarRadioSelect(forms.RadioSelect):
    def __init__(self, *args, **kwargs):
        self.stars = kwargs.pop('stars', 5)
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        html = '<div class="star-rating">'
        for i in range(1, self.stars + 1):
            html += f'<input type="radio" id="{name}_{i}" name="{name}" value="{i}"'
            if str(value) == str(i):
                html += ' checked="checked"'
            html += f'><label for="{name}_{i}" title="{i} stars"></label>'

        html += '</div>'
        return mark_safe(html)

class HotelRatingForm(forms.ModelForm):
    class Meta:
        model = HotelRating
        fields = ['rating']
        widgets = {
            'rating': StarRadioSelect(stars=5),
        }
