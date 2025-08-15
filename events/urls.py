from django.urls import path
from events.views import dashboard, create_event, update_event, delete_event, create_category, update_category, create_participant, update_participant, delete_participant, event_details, delete_category

urlpatterns = [
    path("event_details/<int:id>/",event_details, name='event-details'),
    path("dashboard/",dashboard, name='dashboard'),

    path("create-event/",create_event, name="create-event"),
    path("update-event/<int:id>/",update_event, name="update-event"),
    path("delete-event/<int:id>/",delete_event, name="delete-event"),

    path("create-category/",create_category, name="create-category"),
    path("update-category/<int:id>/",update_category, name="update-category"),
    path("delete-category/<int:id>/",delete_category, name="delete-category"),

    path("create-participant/",create_participant, name="create-participant"),
    path("update-participant/<int:id>/",update_participant, name="update-participant"),
    path("delete-participant/<int:id>/",delete_participant, name="delete-participant"),
]
