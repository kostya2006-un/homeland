from django.test import TestCase
from django.urls import reverse
from app.models import Hotel, Profile, Order, Apartament, Country, City, Review, NumberPeople, Category
from django.contrib.auth.models import User

class IndexViewTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')

class HotelListViewTestCase(TestCase):
    def test_hotel_list_view_get(self):
        response = self.client.get(reverse('hotels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/hotel_list.html')

    def test_hotel_list_view_post(self):
        country = Country.objects.create(country_name='Россия')
        response = self.client.post(reverse('hotels_list'), {'name': country.country_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/hotel_list.html')


class HotelDetailViewTestCase(TestCase):
    def setUp(self):

        self.country = Country.objects.create(country_name='Россия')
        self.city = City.objects.create(city_name='Москва')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.hotel = Hotel.objects.create(hotel_name='hotel1', city=self.city, country=self.country,
                                      description='фысывф', address='фываыфва')

    def test_hotel_detail_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('hotel_detail', kwargs={'pk': self.hotel.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/hotel_detail.html')

    def test_hotel_detail_view_post(self):
        self.client.login(username='testuser', password='testpassword')

        review_data = {
            'text': 'Test review text',
        }

        response = self.client.post(reverse('hotel_detail', kwargs={'pk': self.hotel.pk}), data=review_data)
        self.assertEqual(response.status_code, 302)

        created_review = Review.objects.filter(text='Test review text').exists()
        self.assertTrue(created_review)

        self.assertEqual(Review.objects.get(text='Test review text').hotel, self.hotel)
        self.assertEqual(Review.objects.get(text='Test review text').user, self.user)


class ApartamentViewTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(country_name='Россия')
        self.city = City.objects.create(city_name='Москва')
        self.hotel = Hotel.objects.create(hotel_name='hotel1', city=self.city,
                                          country=self.country,
                                          description='фысывф', address='фываыфва')
        self.max_people = NumberPeople.objects.create(number = '2')
        self.category = Category.objects.create(name = 'обычный')
        self.apartament = Apartament.objects.create(name = 'test', hotel=self.hotel, category = self.category,
                                                    description = 'testss', price = 2000,
                                                    max_people=self.max_people,
                                                    )

    def test_apartament_view_get(self):
        response = self.client.get(reverse('apartaments', kwargs={'pk': self.hotel.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/apartament_list.html')

