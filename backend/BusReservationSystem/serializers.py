from rest_framework import serializers
from .models import BusReservationSystem

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusReservationSystem
        fields = ('id', 'title', 'description', 'completed')