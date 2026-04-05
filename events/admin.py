from django.contrib import admin
from events.models import Participant, Category, Event

admin.site.register(Participant)
admin.site.register(Category)
admin.site.register(Event)

# Register your models here.
