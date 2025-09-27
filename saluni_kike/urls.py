# saluni_kike/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('salons/', views.salon_list, name='salon_list'),
    path('salons/<int:salon_id>/', views.salon_detail, name='salon_detail'),
    path('salons-json/', views.salon_list_json, name='salon_list_json'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('salon/register/', views.salon_register, name='salon_register'),
    path('salon/<int:salon_id>/update/', views.salon_update_profile, name='salon_update_profile'),

]
