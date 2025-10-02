from django.contrib import admin
from django.urls import path, include  # 👈 ONGEZA 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('saluni_kike.urls')), 
    path('', include('dashboard.urls')),   
]