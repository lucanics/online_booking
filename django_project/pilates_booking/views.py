from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, 
    DetailView, 
    DeleteView,
    CreateView,
    UpdateView
)
from .models import Booking
from .admin import CustomUserAdmin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.decorators import login_required

from datetime import date, datetime, timedelta, timezone


def get_week_list(year_number):
    max_weeknumber = date( int(year_number) , 12, 28).isocalendar()[1] # check in with weeknumber the last day of the year is in
    day_of_the_week = range(1,6)
    week_number = range(1, max_weeknumber+1)
    current_week = datetime.now().isocalendar()[1]
    week_list = []
    
    for w in week_number:
        for d in day_of_the_week:
            show_date = date.fromisocalendar(int(year_number), w, d) # year, week number, day of the week
            week_list.append([show_date, show_date.strftime('%A')])
    return week_list, max_weeknumber

def get_time_range(minh, maxh):
    timerange_list = []
    for hour in range(minh, maxh):
        timerange_list.append([hour, 0]) # hour and min
        timerange_list.append([hour, 15])
        timerange_list.append([hour, 30])
        timerange_list.append([hour, 45])
    timerange_list.append([maxh + 1, 0])
    return timerange_list

def person_registration(request, pk):
    '''add/removes registration for booking with primary key pk'''
    booking_slot = Booking.objects.get(pk=pk)
    user = request.user # currently logged in user
    week_number = booking_slot.date.isocalendar()[1] # get week number of booking slot
    try:
        dummy = booking_slot.attendees.get(username=user.username) # only exists if user has made this booking before
        if booking_slot.date < datetime.now(timezone.utc) + timedelta(days=1): # if less than 24h until booking
            time_diff = booking_slot.date - datetime.now(timezone.utc)
            txt_message = f"Buchung kann nicht mehr storniert werden, weil die Einheit '{booking_slot}' in unter 24 Stunden beginnt"
            return render(request, 'pilates_booking/booking_change.html',
            {'txt_message':txt_message, 'week_number':week_number})
        booking_slot.attendees.remove(user)
        booking_slot.save()
        txt_message = f"Buchung wurde storniert!"
    except Exception:
        if booking_slot.date < datetime.now(timezone.utc): # if less than 24h until booking
            time_diff = booking_slot.date - datetime.now(timezone.utc)
            txt_message = f"Buchung kann nicht durchgeführt werden, weil die Einheit '{booking_slot}' schon begonnen hat bzw. vorbei ist."
            return render(request, 'pilates_booking/booking_change.html',
            {'txt_message':txt_message, 'week_number':week_number})
        booking_slot.attendees.add(user)
        booking_slot.save()
        txt_message = f"{user.username} hat '{booking_slot}' erfolgreich gebucht!"
    return render(request, 'pilates_booking/booking_change.html',
           {'txt_message':txt_message, 'week_number':week_number})

def calendar(request):
    week_number = request.GET.get('week')
    if week_number == None:
        week_number = datetime.now().isocalendar()[1] # current week
    
    year_number = request.GET.get('year')
    if year_number == None:
        year_number = datetime.now().year # current year

    week_list, max_weeknumber = get_week_list(year_number) 
    booking_slots = Booking.objects.all()
    paginator = Paginator(week_list, 5) # 5 days at a time (one week MO-FR)
    week_obj = paginator.get_page(week_number).object_list
    user = request.user

    context = {
        'booking_slots': booking_slots,
        'hours': get_time_range(6, 19),
        'week_list': week_list, # [date, weekday_string]
        'week_number': week_number,
        'year_number': year_number,
        'week_obj': week_obj, # for pagination
        'max_weeknumber': max_weeknumber, # to increase year if necessary
    }   
    return render(request, 'pilates_booking/home.html', context)


class BookingSlotsListView(ListView):
     model = Booking
     template_name = 'pilates_booking/booking_slots.html' # default: <app>/<model>_<viewtype>.html
     context_object_name = 'booking_slots'
     ordering = ['-duration']


class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'pilates_booking/user_bookings.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'bookings'
    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print(f"user = {user}")
        return CustomUserAdmin.get_booking_titles_and_dates(self, user)
        
