from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('', views.event_list, name='event_list'),
    path('', views.EventListView.as_view(), name='event_list'),
    # path('event/add/', views.add_event, name='add_event'),
    path('event/add/', views.CreateEventView.as_view(), name='add_event'),
    # path('event/detailed/<int:pk>/', views.detail_event, name='detail_event'),
    path('event/detailed/<int:pk>/', views.DetailEventView.as_view(), name='detail_event'),
    # path('event/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('event/delete/<int:pk>/', views.DeleteEventView.as_view(), name='delete_event'),
    # path('event/change/<int:pk>/', views.change_event, name='change_event'),
    path('event/change/<int:pk>/', views.UpdateEventView.as_view(), name='change_event'),
    path('event/buy/<int:pk>/', views.buy_ticket, name='buy_ticket'),
]