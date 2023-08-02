from django.contrib import admin

from .models import City, Bus, Trip, Reservation, Employee, Driver, Host, Station, RestArea, Seat


class BusReservationSystemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')


admin.site.register(City)
admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(Reservation)
admin.site.register(Employee)
admin.site.register(Driver)
admin.site.register(Host)
admin.site.register(Station)
admin.site.register(RestArea)
admin.site.register(Seat)
