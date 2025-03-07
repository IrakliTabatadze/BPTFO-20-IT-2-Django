from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # path('registration/', views.register_user, name='registration'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    # path('login/', views.login_user, name='login'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password_request/', views.reset_password_request, name='reset_password_request'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
]