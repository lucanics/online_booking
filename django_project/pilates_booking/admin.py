from django.contrib import admin
from .models import Booking
from datetime import timedelta 
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

import pandas as pd
import pytz


def duplicate_booking(self, request, queryset):
    for counter, object in enumerate(queryset, start=1):
        object.id = None
        object.date += timedelta(weeks=1)
        object.save()
    if counter == 1:
        message_bit = "%s booking was" % counter
    else:
        message_bit = "%s bookings were" % counter
    self.message_user(request, "%s duplicated." % message_bit)
duplicate_booking.short_description = "Duplicate booking(s) for the following week"


def duplicate_booking_until(self, request, queryset):
    if 'apply' in request.POST:
        date_until = request.POST['date_until']
        date_until = pd.to_datetime(date_until).replace(tzinfo=pytz.UTC)
        #date_until = date_until.replace(tzinfo=pytz.UTC)
 
        # The user clicked submit on the intermediate form.
        # Perform our update action:
        for counter, object in enumerate(queryset, start=1):
            week_count = 0
            while object.date + timedelta(weeks=1) <= date_until:
                week_count += 1
                object.id = None
                object.date += timedelta(weeks=1)
                object.save()

        # Redirect to our admin view after our update has 
        # completed with a nice little info message saying 
        # our models have been updated:
        if counter == 1:
            message_bit = "%s booking was" % counter
        else:
            message_bit = "%s bookings were" % counter
        self.message_user(request, f"{message_bit} duplicated {week_count} times.")
        return HttpResponseRedirect(request.get_full_path())

    return render(request,
                      'pilates_booking/booking_intermediate.html',
                      context={'bookings':queryset})
duplicate_booking_until.short_description = "Duplicate booking(s) weekly until specific date"


class BookingAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'slots_available', 'get_attendees', 'content')
    date_hierarchy = 'date'
    ordering = ['-date']
    save_as = True
    actions = [duplicate_booking, duplicate_booking_until]


class BookingInline(admin.StackedInline):
    model = Booking.attendees.through
    can_delete = False
    verbose_name_plural = 'Bookings'
    fk_name = 'user' #or booking?


class CustomUserAdmin(UserAdmin):
    inlines = (BookingInline, )
    list_display = UserAdmin.list_display + ('get_booking_ids',)

    #def get_attendees(self):
    #    return ", ".join([p.username for p in self.attendees.all()])

    def get_booking_ids(self,   obj):
        booking_ids = [p.pk for p in obj.booking_set.all()]
        booking_ids.sort()
        return booking_ids
    get_booking_ids.short_description = 'Bookings (ID)'

    def get_booking_titles_and_dates(self, obj):
        return [[p.title, p.date] for p in obj.booking_set.all()]
        
        #", ".join(list(*list(zip(titles,dates))))
        
        #", ".join([p.title for p in obj.booking_set.all()])
        


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Booking, BookingAdmin)
