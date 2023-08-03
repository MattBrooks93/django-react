from django import forms
from .models import Trip, Reservation


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['start_city', 'end_city', 'trip_type', 'departure_time', 'arrival_time', 'bus', 'stations']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['trip', 'seats']
