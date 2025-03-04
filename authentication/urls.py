from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password_request/', views.reset_password_request, name='reset_password_request'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
]