from datetime import date, time

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, MenuItem


class MenuItemModelTest(APITestCase):
    def test_menu_item_str(self):
        item = MenuItem.objects.create(title='Greek Salad', price=12.50)
        self.assertIn('Greek Salad', str(item))


class MenuItemAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='chef', password='StrongPass123')
        self.item = MenuItem.objects.create(title='Bruschetta', price=8.00)

    def test_anyone_can_list_menu_items(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_unauthenticated_user_cannot_create_menu_item(self):
        response = self.client.post(
            reverse('menu-items'), {'title': 'Falafel', 'price': '9.00'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_menu_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('menu-items'), {'title': 'Falafel', 'price': '9.00'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)

    def test_negative_price_is_rejected(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('menu-items'), {'title': 'Broken Item', 'price': '-5.00'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_single_menu_item(self):
        response = self.client.get(reverse('menu-item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Bruschetta')


class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='diner', password='StrongPass123')
        self.other_user = User.objects.create_user(username='other', password='StrongPass123')
        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_user_cannot_list_bookings(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking(self):
        payload = {
            'name': 'Mario Rossi',
            'no_of_guests': 4,
            'booking_date': str(date(2026, 12, 24)),
            'booking_time': '19:30:00',
        }
        response = self.client.post(reverse('bookings'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)

    def test_user_only_sees_own_bookings(self):
        Booking.objects.create(
            user=self.user, name='My Booking', no_of_guests=2,
            booking_date=date(2026, 12, 24), booking_time=time(19, 0),
        )
        Booking.objects.create(
            user=self.other_user, name='Someone Else', no_of_guests=2,
            booking_date=date(2026, 12, 24), booking_time=time(20, 0),
        )
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'My Booking')

    def test_invalid_guest_count_is_rejected(self):
        payload = {
            'name': 'Bad Booking',
            'no_of_guests': 0,
            'booking_date': str(date(2026, 12, 24)),
            'booking_time': '19:30:00',
        }
        response = self.client.post(reverse('bookings'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_booking(self):
        booking = Booking.objects.create(
            user=self.user, name='To Delete', no_of_guests=2,
            booking_date=date(2026, 12, 24), booking_time=time(19, 0),
        )
        response = self.client.delete(reverse('booking-detail', args=[booking.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)


class UserRegistrationAPITest(APITestCase):
    def test_register_new_user(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123',
        }
        response = self.client.post(reverse('api-register'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_requires_password(self):
        response = self.client.post(reverse('api-register'), {'username': 'nopass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_auth_token(self):
        User.objects.create_user(username='tokenuser', password='StrongPass123')
        response = self.client.post(
            reverse('api-token-auth'), {'username': 'tokenuser', 'password': 'StrongPass123'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
