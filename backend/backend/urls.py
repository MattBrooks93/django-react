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
from django.urls import path, include
from rest_framework import routers
from BusReservationSystem import views

router = routers.DefaultRouter()
router.register(r'BusReservationSystems', views.BusReservationSystemView, 'BusReservationSystem')

from backend.BusReservationSystem.views import customer_login, employee_login

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('api/', include(router.urls)),
]
=======
    path('api/login/customer', customer_login, name='customer_login'),
    path('api/login/employee', employee_login, name='employee_login')
]
>>>>>>> abae1e84f41feaed5d1b5eac8b40c0a9a5bad837
