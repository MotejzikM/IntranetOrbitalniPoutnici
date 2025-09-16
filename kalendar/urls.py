from django.urls import path
from . import views

app_name = 'kalendar'

urlpatterns = [
    path("", views.index, name="index"),  # Main page of the calendar app
    path("events/", views.event_list, name="event_list"),  # List of events
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("events/add/", views.add_event, name="add_event"),  # Add a new event
    path("events/<int:event_id>/edit/", views.edit_event, name="edit_event"),  # Edit an existing event
    path("events/<int:event_id>/delete/", views.delete_event, name="delete_event"),  # Delete an event
    path('api/events/', views.event_list_json, name='event_list_json'),

]