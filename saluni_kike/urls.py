# saluni_kike/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('salons/', views.salon_list, name='salon_list'),
    path('salons/<int:salon_id>/', views.salon_detail, name='salon_detail'),
    path('salons-json/', views.salon_list_json, name='salon_list_json'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('booking/<int:salon_id>/new/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('salon/register/', views.salon_register, name='salon_register'),
    path('salon/<int:salon_id>/update/', views.salon_update_profile, name='salon_update_profile'),

    # Login & Logout
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
]
