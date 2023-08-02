from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BusReservationSystemSerializer
from .models import Todo

# Create your views here.

class TodoView(viewsets.ModelViewSet):
    serializer_class = BusReservationSystemSerializer
    queryset = BusReservationSystem.objects.all()