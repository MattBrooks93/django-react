from rest_framework import serializers
from .models import Employee, Customer, City, Bus, Station, Trip, Reservation, Driver, Host, RestArea, Seat

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'employee_id', 'hire_date']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['plate_number', 'bus_number', 'seats']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['name', 'city']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['start_city', 'end_city', 'trip_type', 'departure_time', 'arrival_time', 'bus', 'stations']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['user', 'trip', 'seats', 'paid', 'cancelled', 'cancellation_time']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['employee', 'license_number']

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['employee', 'training_completed']

class RestAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestArea
        fields = ['name', 'station']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['number', 'bus', 'reservation']
