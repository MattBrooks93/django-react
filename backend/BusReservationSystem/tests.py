from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import City, Bus, Trip, Station, TripStation, Reservation, Employee, Customer, Seat
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import json


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', password='testpassword', is_staff=True)
        self.customer_user = User.objects.create_user(username='customer', password='testpassword')

        # Create cities for testing
        self.city1 = City.objects.create(name='City A')
        self.city2 = City.objects.create(name='City B')

        # Create a test bus
        self.bus = Bus.objects.create(plate_number='XYZ123', bus_number='123', seats=50)

        # Create a test trip
        self.trip = Trip.objects.create(
            start_city=self.city1,
            end_city=self.city2,
            trip_type=Trip.NORMAL,
            departure_time='2023-08-03T12:00:00Z',
            arrival_time='2023-08-03T15:00:00Z',
            bus=self.bus
        )

    def test_employee_signup(self):
        response = self.client.post('/api/register/employee', {'username': 'new_employee', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_customer_login(self):
        response = self.client.post('/api/login/customer', {'username': 'customer', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_create_reservation(self):
        self.client.login(username='customer', password='testpassword')
        data = {
            'tripId': self.trip.id,
            'numSeats': 2
        }
        response = self.client.post('/api/reservations/create', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())


class ModelTests(TestCase):
    def setUp(self):
        self.city1 = City.objects.create(name='City A')
        self.city2 = City.objects.create(name='City B')
        self.bus = Bus.objects.create(plate_number='XYZ123', bus_number='123', seats=50)

        self.station1 = Station.objects.create(name='Station 1', city=self.city1)
        self.station2 = Station.objects.create(name='Station 2', city=self.city2)

    def test_validate_bus_availability(self):
        now = datetime.now()
        # Create a trip that ends after the current time
        trip1 = Trip.objects.create(
            start_city=self.city1,
            end_city=self.city2,
            trip_type=Trip.NORMAL,
            departure_time=now - timedelta(hours=1),
            arrival_time=now + timedelta(hours=1),
            bus=self.bus
        )
        # This should raise a validation error since the new trip starts before the previous trip ends
        with self.assertRaises(ValidationError):
            trip2 = Trip.objects.create(
                start_city=self.city1,
                end_city=self.city2,
                trip_type=Trip.NORMAL,
                departure_time=now + timedelta(hours=1),
                arrival_time=now + timedelta(hours=2),
                bus=self.bus
            )

    def test_reservation_creation(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        trip = Trip.objects.create(
            start_city=self.city1,
            end_city=self.city2,
            trip_type=Trip.NORMAL,
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=2),
            bus=self.bus
        )
        reservation = Reservation.objects.create(user=user, trip=trip, seats=2)
        self.assertEqual(reservation.paid, False)
        self.assertEqual(reservation.cancelled, False)
        self.assertIsNone(reservation.cancellation_time)


def reserve_seats(self, user, trip, num_seats):
    if num_seats <= 0:
        raise ValidationError("Number of seats must be greater than 0")

    if trip.available_seats < num_seats:
        raise ValidationError("Not enough available seats on the trip")

    reservation = Reservation.objects.create(user=user, trip=trip, seats=num_seats)
    trip.available_seats -= num_seats
    trip.save()
    return reservation


def cancel_reservation(self, reservation):
    if reservation.paid:
        raise ValidationError("Cannot cancel a paid reservation")

    if reservation.cancelled:
        raise ValidationError("Reservation is already cancelled")

    reservation.cancelled = True
    reservation.cancellation_time = datetime.now()
    reservation.save()
    return reservation
