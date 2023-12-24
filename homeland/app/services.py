from django_filters import rest_framework as filters
from app.models import Hotel,Apartament

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class HotelFilter(filters.FilterSet):
    country = CharFilterInFilter(field_name='country__country_name', lookup_expr='in')

    class Meta:
        model = Hotel
        fields = ['country']

class ApartamentFilter(filters.FilterSet):
    max_people = CharFilterInFilter(field_name='max_people__number',lookup_expr='in')
    category = CharFilterInFilter(field_name='category__name',lookup_expr='in')
    class Meta:
        model = Apartament
        fields = ['max_people','category']