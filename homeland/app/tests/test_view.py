from django.test import TestCase
from django.urls import reverse


class IndexTestCase(TestCase):
    def test_get(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class HotelTestCase(TestCase):
    def test_hotellist_get(self):
        url = reverse('hotels_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


