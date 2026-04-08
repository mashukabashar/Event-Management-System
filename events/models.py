from django.db import models
from django.contrib.auth.models import User, Group


class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name




class Event(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="event"
    )
    asset=models.ImageField(upload_to='event_assets/', null=True, blank=True)
    participants=models.ManyToManyField(User, related_name="events")
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"
