from django.db import models


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

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'event'