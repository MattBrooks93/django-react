from django.contrib import admin
from .models import BusReservationSystem

class BusReservationSystemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')

# Register your models here.

admin.site.register(BusReservationSystem, BusReservationSystemAdmin)