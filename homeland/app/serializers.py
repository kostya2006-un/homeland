from rest_framework import serializers
from .models import Hotel,Country,Apartament,Review,Profile,Order

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
    #hotel = serializers.SlugRelatedField(slug_field='hotel_name', read_only=True)
    # user = serializers.SlugRelatedField(slug_field='username',read_only=True)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Review
        fields = ('__all__')

class ProfileViewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Profile
        fields = ('__all__')
        read_only_fields = ('user',)

class AllOrdersSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    apartament = serializers.SlugRelatedField(slug_field='name', read_only=True)
    status = serializers.SlugRelatedField(slug_field='status', read_only=True)

    class Meta:
        model = Order
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Order
        fields = ('__all__')
        read_only_fields = ('user','total_amount', )

    def create(self, validated_data):
        # Вычисление total_amount
        apartament = validated_data['apartament']
        arrive_date = validated_data['arrive_date']
        leave_date = validated_data['leave_date']
        days = (leave_date - arrive_date).days
        validated_data['total_amount'] = apartament.price * days

        return super().create(validated_data)

class OrderDetailSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Order
        fields = ('__all__')




