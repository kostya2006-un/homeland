from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Hotel,Country,City
from app.serializers import HotelListSerializer


class HotelApiTestCase(APITestCase):
    def test_get(self):
        country = Country.objects.create(country_name = 'Россия')
        city = City.objects.create(city_name = 'Москва')

        hotel1 = Hotel.objects.create(hotel_name='hotel1', city=City.objects.get(city_name = 'Москва'), country=Country.objects.get(country_name = 'Россия'),
                                      description='фысывф', address='фываыфва', img='')

        hotel2 = Hotel.objects.create(hotel_name='hotel2', city=City.objects.get(city_name='Москва'),
                                      country=Country.objects.get(country_name='Россия'),
                                      description='2', address='2', img='')

        url = reverse('hotellist')
        response = self.client.get(url)
        serializer_data = HotelListSerializer([hotel1, hotel2], many=True).data
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertEqual(serializer_data, response.data)