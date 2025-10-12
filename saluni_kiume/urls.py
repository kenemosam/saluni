# saluni_kiume/urls.py
from django.urls import path
from . import views

app_name = 'kiume'

urlpatterns = [
    # Step 1: Minimal registration
    path('register/', views.male_salon_register, name='male_salon_register'),

    # Step 2: Full profile update
    path('update/<int:salon_id>/', views.male_salon_update, name='male_salon_update'),

    # List and detail views
    path('', views.male_salon_list, name='male_salon_list'),
    path('<int:salon_id>/', views.male_salon_detail, name='male_salon_detail'),
    path('salons-json/', views.male_salon_list_json, name='male_salon_list_json'),

    # Bookings
    path('<int:salon_id>/booking/', views.create_male_booking, name='create_male_booking'),
    path('booking/<int:booking_id>/', views.male_booking_detail, name='male_booking_detail'),
]

