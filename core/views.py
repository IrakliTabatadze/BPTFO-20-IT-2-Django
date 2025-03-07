from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Event, EventTicket, EventImage
from .forms import EventForm, EventImageFormSet
from django.contrib.auth.decorators import login_required
from .permissions import event_administrator, delete_event_permission, change_event_permission
from django.db.models import Q
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)

# FBV - Function Based Views
# CBV - Class Based Views

# @login_required(login_url='login')
# def event_list(request):
#     title = request.GET.get('title')
#     location = request.GET.get('location')
#
#     logger.info(f'Event Filters: {title}, {location}')
#
#     filters = Q()
#
#     if title:
#         filters |= Q(title__icontains=title)
#
#     if location:
#         filters |= Q(location__icontains=location)
#
#     if title and location:
#         filters &= Q(title__icontains=title) & Q(location__icontains=location)
#
#     logger.info(filters)
#
#     if title or location:
#         events = Event.objects.filter(filters)
#     else:
#         events = Event.objects.all()
#
#     paginator = Paginator(events, 8)
#
#     try:
#         page_number = request.GET.get('page')
#
#         events = paginator.page(page_number)
#     except PageNotAnInteger:
#         events = paginator.page(1)
#     except EmptyPage:
#         events = paginator.page(paginator.num_pages)
#
#     return render(request, 'events/event_list.html', {'events': events})


# class EventListView(View):
#
#     @staticmethod
#     def get(request):
#         title = request.GET.get('title')
#         location = request.GET.get('location')
#
#         logger.info(f'Event Filters: {title}, {location}')
#
#         filters = Q()
#
#         if title:
#             filters |= Q(title__icontains=title)
#
#         if location:
#             filters |= Q(location__icontains=location)
#
#         if title and location:
#             filters &= Q(title__icontains=title) & Q(location__icontains=location)
#
#         logger.info(filters)
#
#         if title or location:
#             events = Event.objects.filter(filters)
#         else:
#             events = Event.objects.all()
#
#         paginator = Paginator(events, 8)
#
#         try:
#             page_number = request.GET.get('page')
#
#             events = paginator.page(page_number)
#         except PageNotAnInteger:
#             events = paginator.page(1)
#         except EmptyPage:
#             events = paginator.page(paginator.num_pages)
#
#         return render(request, 'events/event_list.html', {'events': events})



class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 8

    def get_queryset(self):
        title = self.request.GET.get('title')
        location = self.request.GET.get('location')

        filters = Q()

        if title:
            filters |= Q(title__icontains=title)

        if location:
            filters |= Q(location__icontains=location)

        if title and location:
            filters &= Q(title__icontains=title) & Q(location__icontains=location)


        queryset = self.model.objects.filter(filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context





# @login_required(login_url='login')
# @event_administrator
# def add_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('event_list')
#     else:
#         form = EventForm()
#         return render(request, 'events/add_event.html', {'form': form})


# def add_event(request):
#     if request.method == 'POST':
#         event_form = EventForm(request.POST)
#         image_formset = EventImageFormSet(request.POST, request.FILES)
#
#         if event_form.is_valid() and image_formset.is_valid():
#             event = event_form.save()
#
#             for form in image_formset:
#                 if form.cleaned_data.get('image'):
#                     image = form.save(commit=False)
#                     image.event = event
#                     image.save()
#
#         return redirect('event_list')
#
#     else:
#         event_form = EventForm()
#         image_formset = EventImageFormSet()
#
#         return render(request, 'events/add_event.html', {'event_form': event_form, 'image_formset': image_formset})

class CreateEventView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('core:event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['image_formset'] = EventImageFormSet(queryset=EventImage.objects.none())

        print(context)

        return context

    def form_valid(self, form):
        event = form.save()

        image_formset = EventImageFormSet(self.request.POST, self.request.FILES)

        if image_formset.is_valid():
            for form in image_formset:
                image = form.save(commit=False)
                image.event = event
                image.save()

        return redirect(self.success_url)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# def detail_event(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#
#     return render(request, 'events/event_detail.html', {'event': event})


class DetailEventView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


# @login_required(login_url='login')
# @delete_event_permission
# def delete_event(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#
#     event.delete()
#
#     return redirect('event_list')

class DeleteEventView(DeleteView):
    model = Event
    success_url = reverse_lazy('core:event_list')
    template_name = 'events/confirm_delete.html'


# @login_required(login_url='login')
# @change_event_permission
# def change_event(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#
#     if request.method == 'POST':
#         form = EventForm(request.POST, instance=event)
#         if form.is_valid():
#             form.save()
#
#             print(f'Previous Page: {request.META.get('HTTP_REFERER')}')
#
#             return redirect('detail_event', pk=pk)
#     else:
#         form = EventForm(instance=event)
#
#         return render(request, 'events/change_event.html', {'form': form})

class UpdateEventView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/change_event.html'

    def get_success_url(self):
        return reverse_lazy('core:detail_event', kwargs={'pk': self.object.id})


@login_required(login_url='login')
def buy_ticket(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.sold_out():
        return HttpResponse('All Tickets are sold out')

    event_ticket, created = EventTicket.objects.get_or_create(event=event, owner=request.user)

    # number_of_tickets = request.POST.get('number_of_tickets')

    if created:
        event_ticket.ticket_count = 1
    else:
        event_ticket.ticket_count += 1

    event_ticket.save()

    event.ticket_count -= 1
    event.save()

    send_mail('Buy Ticket', f'{request.user.username} has successfully bought ticket on: {event.title}',
              settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)

    return redirect('event_list')

# SMTP Server - Simple Mail Transfer Protocol
