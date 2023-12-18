from rest_framework import serializers
from .models import Hotel,Country,Apartament,Review

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

class ApartamentSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name',read_only=True)
    hotel = serializers.SlugRelatedField(slug_field='hotel_name',read_only=True)

    class Meta:
        model = Apartament
        fields = ('__all__')

class ApartamentDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    hotel = serializers.SlugRelatedField(slug_field='hotel_name', read_only=True)
    class Meta:
        model = Apartament
        fields = ('__all__')

class ReviewSerializer(serializers.ModelSerializer):
    hotel = serializers.SlugRelatedField(slug_field='hotel_name', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username',read_only=True)
    class Meta:
        model = Review
        fields = ('__all__')