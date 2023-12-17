from rest_framework import serializers
from .models import Hotel,Country

class HotelListSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='city_name',read_only=True)
    country = serializers.SlugRelatedField(slug_field='country_name',read_only=True)
    class Meta:
        model = Hotel
        fields = ('__all__')

class HotelDetailSerializer(serializers.ModelSerializer):

    city = serializers.SlugRelatedField(slug_field='city_name', read_only=True)
    country = serializers.SlugRelatedField(slug_field='country_name', read_only=True)
    class Meta:
        model = Hotel
        fields = ('__all__')

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('__all__')