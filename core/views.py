from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .permissions import event_administrator
from django.db.models import Q

# @login_required(login_url='login')
def event_list(request):

    event_query = request.GET.get('title')

    if event_query:
        events = Event.objects.filter(Q(title__icontains=event_query) | Q(location__icontains=event_query))
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