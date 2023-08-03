"""
URL configuration for BusReservationSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from BusReservationSystem.views import customer_login, employee_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/customer', customer_login, name='customer_login'),
    path('api/login/employee', employee_login, name='employee_login'),
    path('api/register/employee', employee_signup, name='employee_login'),
    path('api/register/customer', customer_signup, name='customer_login'),

    path('api/trips', trips, name='trips'),
    path('api/reservations', reservations, name='reservations'),
    path('api/reservations/<int:reservation_id>', reservation, name='reservation'),
    path('api/trips/<int:trip_id>', trip, name='trip'),
    path('api/trips/<int:trip_id>/reservations', trip_reservations, name='trip_reservations'),
    path('api/trips/<int:trip_id>/reservations/<int:reservation_id>', trip_reservation, name='trip_reservation'),
    path('api/trips/<int:trip_id>/stations', trip_stations, name='trip_stations'),
    path('api/trips/<int:trip_id>/stations/<int:station_id>', trip_station, name='trip_station'),
    path('api/trips/<int:trip_id>/stations/<int:station_id>/reservations', trip_station_reservations)
]
