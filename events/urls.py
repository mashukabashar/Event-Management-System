from django.urls import path
from events.views import organizer_dashboard, create_event, update_event, delete_event, create_category, update_category, event_details, delete_category, rsvp_event

urlpatterns = [
    path("event_details/<int:id>/",event_details, name='event-details'),
    
    path("organizer-dashboard/",organizer_dashboard, name='organizer-dashboard'),

    path("create-event/",create_event, name="create-event"),
    path("update-event/<int:id>/",update_event, name="update-event"),
    path("delete-event/<int:id>/",delete_event, name="delete-event"),

    path("create-category/",create_category, name="create-category"),
    path("update-category/<int:id>/",update_category, name="update-category"),
    path("delete-category/<int:id>/",delete_category, name="delete-category"),

    path('rsvp/<int:event_id>/', rsvp_event, name='rsvp-event')
]
