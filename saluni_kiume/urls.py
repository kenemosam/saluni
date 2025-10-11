# saluni_kiume/urls.py
from django.urls import path
from . import views

app_name = 'kiume'

urlpatterns = [
    path('', views.male_salon_list, name='male_salon_list'),
    path('<int:salon_id>/', views.male_salon_detail, name='male_salon_detail'),
    path('salons-json/', views.male_salon_list_json, name='male_salon_list_json'),
    path('<int:salon_id>/booking/', views.create_male_booking, name='create_male_booking'),
    path('booking/<int:booking_id>/', views.male_booking_detail, name='male_booking_detail'),
]
