from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/add/', views.add_event, name='add_event'),
    path('event/detailed/<int:pk>/', views.detail_event, name='detail_event'),
]