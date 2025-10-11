from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kike/', include('saluni_kike.urls')), 
    path('kiume/', include('saluni_kiume.urls')), 
    path('', include('dashboard.urls')),   
]