from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from app.models import Hotel, Profile, Order, Apartament, Country, City, Review, NumberPeople, Category, Status
from django.contrib.auth.models import User
from datetime import timedelta
from datetime import datetime

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
                                          description='1', address='фываыфва')
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

    def test_apartament_detail_get(self):
        response = self.client.get(reverse('apartament_detail',kwargs={'pk': self.hotel.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/apartament_detail.html')

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user = self.user,money = 10000)

    def test_get(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/profile.html')

    def test_increment_balance(self):
        initial_balance = self.profile.money

        response = self.client.get(reverse('increment_balance'))

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.money, initial_balance + 1000)

        self.assertRedirects(response, reverse('profile'))

class OrderViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user = self.user,money = 10000)
        self.country = Country.objects.create(country_name='Россия')
        self.city = City.objects.create(city_name='Москва')
        self.hotel = Hotel.objects.create(hotel_name='hotel1', city=self.city,
                                          country=self.country,
                                          description='1', address='фываыфва')
        self.max_people = NumberPeople.objects.create(number='2')
        self.category = Category.objects.create(name='обычный')
        self.apartament = Apartament.objects.create(name='test', hotel=self.hotel, category=self.category,
                                                    description='testss', price=2000,
                                                    max_people=self.max_people,
                                                    )
        self.order = Order.objects.create(
            user=self.user,
            apartament = self.apartament,
            arrive_date = '2024-01-15',
            leave_date = '2024-01-17',
            total_amount=4000,
            status=Status.objects.get_or_create(status="неначатый")[0]
        )

    def test_get(self):
        response = self.client.get(reverse('order', kwargs={'pk': self.apartament.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/order.html')

    def test_order_view_post_invalid_date(self):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        data = {
            'start_date': str(yesterday),
            'end_date': str(today),
        }

        response = self.client.post(reverse('order', kwargs={'pk': self.apartament.pk}), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count() - 1, 0)

    def test_order_view_post_invalid_dates_order(self):
        data = {
            'start_date': '2024-01-15',
            'end_date': '2024-01-10',
        }

        response = self.client.post(reverse('order', kwargs={'pk': self.apartament.pk}), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count() - 1, 0)

    def test_order_view_post_valid_order_creation(self):
        data = {
            'start_date': '2024-01-15',
            'end_date': '2024-01-20',
            'create_order': '',
        }
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        days = (end_date - start_date).days
        price = self.apartament.price * days

        response = self.client.post(reverse('order', kwargs={'pk': self.apartament.pk}), data=data)
        self.profile.money -= price
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(Order.objects.count() - 1, 1)
        self.assertEqual(self.profile.money, 0)

    def test_order_delete_view(self):
        url = reverse('order_delete', kwargs={'pk': self.order.pk})
        response = self.client.post(url)

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.money, 14000)
        self.assertRedirects(response, reverse('profile'))



