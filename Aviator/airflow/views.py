import pytz
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from airflow.models import *
import random
from datetime import datetime

# Create your views here.


def is_valid(t):
    return t != '' and t is not None


def home_page(request):
    return render(request, 'home.html')


def is_congested(ap, active_at):
    delta = random.choice(list(CongestionIndex.objects.all())).delta
    # CongestionIndex table must have only one item at all times
    dep_list = Flight.objects.select_for_update().filter(dep_airport__city=ap)
    arr_list = Flight.objects.select_for_update().filter(arr_airport__city=ap)

    count = 0
    print(delta)

    for t in dep_list:
        print(abs(t.dep_time - active_at))
        if abs(t.dep_time - active_at) < delta:
            count += 1

    for t in arr_list:
        print(t.arr_time - active_at)
        if abs(t.arr_time - active_at) < delta:
            count += 1

    if count+1 > ap.run_c:
        return True
    else:
        return False


@transaction.atomic
def flight_show(request):
    query_set = Flight.objects.order_by('fare').filter(fl_status='S')
    al_list = ['']+list(Airline.objects.all())
    ap_list = ['']+list(Airport.objects.all())

    dep_ap = request.GET.get('dep_ap')
    arr_ap = request.GET.get('arr_ap')
    datetime_min = request.GET.get('datetime_min')
    datetime_max = request.GET.get('datetime_max')
    airline = request.GET.get('airline')

    if is_valid(datetime_min):
        query_set = query_set.filter(dep_time__gte=datetime_min)

    if is_valid(datetime_max):
        query_set = query_set.filter(arr_time__lte=datetime_max)

    if is_valid(airline):
        query_set = query_set.filter(airline__name__exact=airline)

    if is_valid(dep_ap) and is_valid(arr_ap):
        query_set = query_set.filter(dep_airport__city__iexact=dep_ap)
        query_set = query_set.filter(arr_airport__city__iexact=arr_ap)

    return render(request, "flight/flight_form.html", {'queryset': query_set,
                                                       'a_ch': al_list,
                                                       'ap_ch': ap_list,
                                                       'len': len(query_set)})


@transaction.atomic
def book_flight(request, flight_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login first')
        return redirect('/login')

    fl = Flight.objects.get(id=flight_id)

    if request.method == 'POST':
        cur = Flight.objects.get(id=flight_id)
        required_seats = int(request.POST['seat_count'])
        occupied_seats = 0

        for t in Booking.objects.select_for_update().filter(fl_id=flight_id):
            occupied_seats += int(t.seat_n)

        if occupied_seats + required_seats > cur.aircraft.seats:
            messages.info(request, 'only '+str(cur.aircraft.seats -
                          occupied_seats)+' seat(s) are remaining')
            return render(request, "booking/booking.html", {'flight': fl})

        else:
            messages.info(request, 'Successfully booked')
            Booking.objects.create(
                user=request.user, fl_id=fl, seat_n=required_seats, total_fare=fl.fare*required_seats).save()
            return redirect('/flights')

    else:
        return render(request, "booking/booking.html", {'flight': fl})


def my_bookings(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You need to log in!')
        return redirect('/login')

    book_list = Booking.objects.filter(user=request.user)

    return render(request, "booking/mybooks.html", {'bookset': book_list, 'len': len(book_list)})


@transaction.atomic
def create_flight(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You need to log in as a staffer!')
        return redirect('/login')

    if request.method == 'POST':
        dep_ap = Airport.objects.get(city=request.POST['dep_ap'])
        arr_ap = Airport.objects.get(city=request.POST['arr_ap'])
        dep_time = datetime.strptime(
            request.POST.get('dep_time'), "%Y-%m-%dT%H:%M")
        arr_time = datetime.strptime(
            request.POST.get('arr_time'), "%Y-%m-%dT%H:%M")
        fl_fare = request.POST['fare']
        aircraft = AirCraft.objects.get(name=request.POST['aircraft'])
        airline = Airline.objects.get(name=request.POST['airline'])

        dep_time = pytz.UTC.localize(dep_time)
        arr_time = pytz.UTC.localize(arr_time)

        if is_congested(dep_ap, dep_time):
            messages.info(request, 'Departure airport is too congested')

        elif is_congested(arr_ap, arr_time):
            messages.info(request, 'Arrival airport is too congested')

        else:
            new_flight = Flight.objects.create(aircraft=aircraft, airline=airline, dep_airport=dep_ap,
                                               arr_airport=arr_ap, dep_time=dep_time, arr_time=arr_time,
                                               fare=fl_fare)
            new_flight.save()
            messages.info(request, 'Flight successfully created')

    airport_list = Airport.objects.all()
    aircraft_list = AirCraft.objects.all()
    airline_list = Airline.objects.all()

    return render(request, 'flight/create_flight.html', {'aircraft_ch': aircraft_list,
                                                         'airline_ch': airline_list,
                                                         'airport_ch': airport_list})
