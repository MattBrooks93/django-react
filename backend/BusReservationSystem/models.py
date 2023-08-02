from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)


class Bus(models.Model):
    plate_number = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=100)
    seats = models.IntegerField()


class Trip(models.Model):
    NORMAL = 'Normal'
    EXPRESS = 'Express'

    TRIP_TYPE_CHOICES = [
        (NORMAL, 'Normal'),
        (EXPRESS, 'Express'),
    ]

    start_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departure_trips')
    end_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrival_trips')
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE_CHOICES, default=NORMAL)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seats = models.IntegerField()
    paid = models.BooleanField(default=False)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100)
    hire_date = models.DateField()


class Driver(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)


class Host(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    training_completed = models.DateField()


class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class RestArea(models.Model):
    name = models.CharField(max_length=100)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)


class Seat(models.Model):
    number = models.IntegerField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True)
