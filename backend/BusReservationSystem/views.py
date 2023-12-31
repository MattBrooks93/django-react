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
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError


def is_employee(user):
    try:
        _ = user.employee
    except Employee.DoesNotExist:
        return False
    return True


def is_customer(user):
    try:
        _ = user.customer
    except Customer.DoesNotExist:
        return False
    return True


@csrf_exempt
@require_http_methods(["POST"])
def employee_signup(request):
    print(request.body)
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create(
        username=username,
        password=make_password(password),
    )
    Employee.objects.create(user=user)

    return JsonResponse({'message': 'Employee created successfully', 'id': user.id})


def employee_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        customer = data.get('is_customer')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not customer:
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

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create(
        username=username,
        password=make_password(password),
    )
    Customer.objects.create(user=user)

    return JsonResponse({'message': 'Customer created successfully', 'id': user.id})


@csrf_exempt
def customer_login(request):
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        customer = data.get('is_customer')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if customer:
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
@customer_required
def create_reservation(request):
    try:
        data = json.loads(request.body)
        trip_id = data.get('tripId')
        num_seats = data.get('numSeats')

        if not all([trip_id, num_seats]):
            return JsonResponse({'error': 'Missing required data'}, status=400)

        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return JsonResponse({'error': 'Trip does not exist'}, status=404)

        if trip.bus.seats < num_seats:
            return JsonResponse({'error': 'Not enough seats available'}, status=400)

        reservation = Reservation.objects.create(
            user=request.user,
            trip=trip,
            seats=num_seats,
            paid=False
        )

    except (TypeError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': 'Database error: ' + str(e)}, status=500)
    except ValidationError as e:
        return JsonResponse({'error': 'Validation error: ' + str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Unexpected error: ' + str(e)}, status=500)

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


@csrf_exempt
@require_http_methods(["POST"])
def process_payment(request):
    try:
        data = json.loads(request.body)
        card_number = data.get('cardNumber')
        expiration_date = data.get('expirationDate')
        cvc = data.get('cvc')

        if not all([card_number, expiration_date, cvc]):
            return JsonResponse({'error': 'Missing required data'}, status=400)

        if not all([len(card_number) == 16, len(expiration_date) == 4, len(cvc) == 3]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        if not all([card_number.isdigit(), expiration_date.isdigit(), cvc.isdigit()]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        if not all([int(expiration_date[:2]) in range(1, 13), int(expiration_date[2:]) in range(20, 30)]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        if not all([int(cvc) in range(100, 1000)]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        if not all([int(card_number[i]) == int(card_number[i]) for i in range(16)]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        if not all([int(expiration_date[i]) == int(expiration_date[i]) for i in range(4)]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # TODO implement the actual logic for processing the payment.

    except Exception as e:
        return JsonResponse({'error': 'Unexpected error: ' + str(e)}, status=500)

    return JsonResponse({'message': 'Payment processed'})


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


@csrf_exempt
@require_http_methods(["POST"])
@login_required
@customer_required
def update_reservation(request, reservation_id):
    try:
        data = json.loads(request.body)
        num_seats = data.get('numSeats')

        if num_seats is None:
            return JsonResponse({'error': 'Missing required data'}, status=400)

        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reservation does not exist'}, status=404)

        if reservation.trip.bus.seats < num_seats:
            return JsonResponse({'error': 'Not enough seats available'}, status=400)

        reservation.seats = num_seats
        reservation.save()

    except (TypeError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': 'Database error: ' + str(e)}, status=500)
    except ValidationError as e:
        return JsonResponse({'error': 'Validation error: ' + str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Unexpected error: ' + str(e)}, status=500)

    return JsonResponse({'message': 'Reservation updated', 'id': reservation.id})


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
