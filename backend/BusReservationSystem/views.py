import json

from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .decorators import employee_required, customer_required
from .forms import ReservationForm, TripForm
from .models import Reservation, Trip
from backend.celery import app


def employee_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_employee:  # Check if the user is an employee
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
            if user.is_customer:  # Check if the user is a customer
                login(request, user)
                return JsonResponse({'message': 'Logged in successfully'})
            else:
                return JsonResponse({'error': 'Not authorized'}, status=403)
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


@require_http_methods(["POST"])
@login_required
def mark_reservation_paid(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        reservation.paid = True
        reservation.save()
        return JsonResponse({'message': 'Payment successful', 'reservation_id': reservation.id})
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found'}, status=404)


@require_http_methods(["POST"])
@login_required
def cancel_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        if reservation.paid:
            return JsonResponse({'error': 'Paid reservations cannot be cancelled'}, status=400)
        reservation.cancelled = True
        reservation.cancellation_time = timezone.now()
        reservation.save()
        return JsonResponse({'message': 'Reservation cancelled', 'reservation_id': reservation.id})
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found'}, status=404)


@app.task
def cancel_unpaid_reservations():
    now = timezone.now()
    threshold_time = now + timedelta(hours=1)

    # Fetch all unpaid and uncancelled reservations with trip start time in less than an hour
    reservations_to_cancel = Reservation.objects.filter(
        paid=False,
        cancelled=False,
        trip__departure_time__lt=threshold_time
    )

    # Update the fetched reservations to be cancelled
    reservations_to_cancel.update(cancelled=True, cancellation_time=now)


@employee_required
@require_http_methods(["GET", "POST"])
def manage_trips(request):
    if request.method == 'GET':
        trips = Trip.objects.all().values()  # fetch all trips as dict
        return JsonResponse({'trips': list(trips)}, safe=False)

    elif request.method == 'POST':
        form = TripForm(json.loads(request.body))
        if form.is_valid():
            new_trip = form.save()
            return JsonResponse({'message': 'Trip created', 'id': new_trip.id}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)


@customer_required
@require_http_methods(["POST"])
def create_reservation(request):
    form = ReservationForm(json.loads(request.body))
    if form.is_valid():
        new_reservation = form.save(commit=False)
        new_reservation.user = request.user
        new_reservation.save()
        return JsonResponse({'message': 'Reservation created', 'id': new_reservation.id}, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)
