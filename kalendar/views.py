from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from kalendar.models import Event
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from .serializers import EventSerializer
from .models import Event

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Create your views here.

@login_required
def index(request):
    """
    Render the main page of the application.
    """

    events = Event.objects.filter(showToTimeline=True).order_by('date')  # Get the latest 10 events to show on the main page

    return render(request, 'kalendar/event_list.html', {'events': events})

@login_required
def event_list(request):
    """
    Display a list of events.
    """
    events = Event.objects.all()
    return render(request, 'kalendar/event_list.html', {'events': events})

@login_required
def event_detail(request, event_id):
    """
    Display details of a specific event.
    """
    event = Event.objects.get(id=event_id)
    return render(request, 'kalendar/event_detail.html', {'event': event})

@login_required
def add_event(request):
    """
    Handle the addition of a new event.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        description = request.POST.get('description', '')
        location = request.POST.get('location', '')
        show_to_timeline = request.POST.get('showToTimeline', 'off') == 'on'
        selected_users = request.POST.getlist('users')  # Get selected user IDs
        

        event = Event.objects.create(
            title=title,
            date=date,
            description=description,
            location=location,
            showToTimeline=show_to_timeline,
        )
        event.participants.set(User.objects.filter(id__in=selected_users))  # Set participants after creation
        return redirect('kalendar:event_detail', event_id=event.id)
    
    users = User.objects.all()  # Assuming you want to show all users for selection

    return render(request, 'kalendar/add_event.html', {
        'form': {
            'title': '',
            'date': '',
            'description': '',
            'location': '',
            'showToTimeline': False
        },
        'action': 'add_event',
        'users': users
    })

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # bezpečnější než get()

    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.date = request.POST.get('date')
        event.description = request.POST.get('description', '')
        event.location = request.POST.get('location', '')
        event.showToTimeline = request.POST.get('showToTimeline', 'off') == 'on'
        selected_users = request.POST.getlist('users')  # Get selected user IDs
        event.participants.set(User.objects.filter(id__in=selected_users))  # Update participants
        event.save()
        return redirect('kalendar:event_detail', event.id)  # bez pojmenovaného argumentu

    users = User.objects.all()

    return render(request, 'kalendar/edit_event.html', {
        'form': {
            'title': event.title,
            'date': event.date,
            'description': event.description,
            'location': event.location,
            'showToTimeline': event.showToTimeline,
            'participants': event.participants.all().values_list('id', flat=True)  # Get selected users
        },
        'action': 'edit_event',
        'event': event,
        'users': users
    })


@login_required
def delete_event(request, event_id):
    """
    Handle the deletion of an event.
    """
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('kalendar:index')
    
    return render(request, 'kalendar/delete_event.html', {'event': event})

@login_required
def event_list_json(request):
    """
    Return a JSON response with a list of events.
    """
    events = Event.objects.all().values('id', 'title', 'date', 'description', 'location')

    # Create url for each event
    for event in events:
        event['url'] = Event.objects.get(id=event['id']).get_absolute_url()

    return JsonResponse(list(events), safe=False)