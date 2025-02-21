from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .permissions import event_administrator, delete_event_permission, change_event_permission
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

# @login_required(login_url='login')
def event_list(request):

    title = request.GET.get('title')
    location = request.GET.get('location')

    logger.info(f'Event Filters: {title}, {location}')

    filters = Q()

    if title:
        filters |= Q(title__icontains=title)

    if location:
        filters |= Q(location__icontains=location)

    if title and location:
        filters &= Q(title__icontains=title) & Q(location__icontains=location)

    logger.info(filters)

    if title or location:
        events = Event.objects.filter(filters)
    else:
        events = Event.objects.all()

    return render(request, 'events/event_list.html', {'events': events})


@login_required(login_url='login')
@event_administrator
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
        return render(request, 'events/add_event.html', {'form': form})


def detail_event(request, pk):

    event = get_object_or_404(Event, pk=pk)

    return render(request, 'events/event_detail.html', {'event': event})


@login_required(login_url='login')
@delete_event_permission
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event.delete()

    return redirect('event_list')


@login_required(login_url='login')
@change_event_permission
def change_event(request, pk):

    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()

            print(f'Previous Page: {request.META.get('HTTP_REFERER')}')

            return redirect('detail_event', pk=pk)
    else:
        form = EventForm(instance=event)

        return render(request, 'events/change_event.html', {'form': form})
