from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class Booking(models.Model):
    title = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    slots_total = models.IntegerField()
    content = models.TextField(blank=True)
    #weekly_event = models.BooleanField(default=True)
    attendees = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ["date"]
    
    def get_attendees(self):
        return ", ".join([p.username for p in self.attendees.all()])
    
    def slots_available(self):
        return f"{self.slots_total - len(self.attendees.all())} / {self.slots_total}"

    def slots_remaining(self):
        return self.slots_total - len(self.attendees.all())

    def __str__(self):
        return f"{self.title} - ({self.date.date()}; {self.date.time()})"


