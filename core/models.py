from django.db import models
from django.contrib.auth.models import User


LOCATION_CHOICES = (
    ('shekvetili_arena', 'Shekvetili Arena'),
    ('meskhis_stationi', 'Meskhis Stationi'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    location = models.CharField(max_length=100, null=False, blank=False, choices=LOCATION_CHOICES)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    max_attendees = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField(default=10, null=True, blank=True)
    # image = models.ImageField(upload_to='event-images', null=True, blank=True)

    def __str__(self):
        return self.title

    def sold_out(self):
        if self.ticket_count <= 0:
            return True
        else:
            return False

    class Meta:
        db_table = 'event'

class EventImage(models.Model):
    image = models.ImageField(upload_to='event-images', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')

class EventTicket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    ticket_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('event', 'owner')
