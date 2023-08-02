from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Reservation, Trip
import json


def employee_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # Check if the user is an employee
                login(request, user)
                return JsonResponse({'message': 'Logged in successfully'})
            else:
                return JsonResponse({'error': 'Not authorized'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def customer_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully'})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_reservation(request):
    data = json.loads(request.body)
    customer_name = data.get('customerName')
    trip_id = data.get('tripId')
    num_seats = data.get('numSeats')

    # TODO: Validate the data, e.g. check if the trip exists and has enough seats

    reservation = Reservation.objects.create(
        user=request.user,
        trip=Trip.objects.get(id=trip_id),
        seats=num_seats,
        paid=False
    )
    return JsonResponse({'message': 'Reservation created', 'id': reservation.id})

class TodoView(viewsets.ModelViewSet):
    serializer_class = BusReservationSystemSerializer
    queryset = BusReservationSystem.objects.all()