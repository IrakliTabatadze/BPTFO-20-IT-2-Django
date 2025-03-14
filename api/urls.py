from django.urls import path
from . import views

urlpatterns = [
    # path('', views.test),
    path('', views.event_list),
    path('event/create/', views.create_event),
    path('event/update/<int:pk>/', views.update_event),
    path('event/delete/<int:pk>/', views.delete_event),
]