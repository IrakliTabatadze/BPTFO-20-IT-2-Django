from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

def event_list(request):

    events = Event.objects.all()

    return render(request, 'events/event_list.html', {'events': events})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
        return render(request, 'events/add_event.html', {'form': form})

