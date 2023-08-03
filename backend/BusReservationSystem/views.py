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
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Customer, Employee


@csrf_exempt
@require_http_methods(["POST"])
def employee_signup(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    # You may want to add more fields based on your User model

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create(
        username=username,
        password=make_password(password),
        # Add more fields here
    )
    Employee.objects.create(user=user)

    return JsonResponse({'message': 'Employee created successfully', 'id': user.id})


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
@require_http_methods(["POST"])
def customer_signup(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    # You may want to add more fields based on your User model

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create(
        username=username,
        password=make_password(password),
        # Add more fields here
    )
    Customer.objects.create(user=user)

    return JsonResponse({'message': 'Customer created successfully', 'id': user.id})


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
    trip_id = data.get('tripId')
    num_seats = data.get('numSeats')

    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Trip does not exist'}, status=404)

    # Get the total number of seats already reserved for this trip
    total_reserved_seats = Reservation.objects.filter(trip=trip, cancelled=False).aggregate(total_seats=Sum('seats'))[
                               'total_seats'] or 0

    # Check if the new reservation would exceed the bus capacity
    if total_reserved_seats + num_seats > trip.bus.seats:
        return JsonResponse({'error': 'Not enough seats available'}, status=400)

    reservation = Reservation.objects.create(
        user=request.user,
        trip=trip,
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
