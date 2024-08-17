from django.contrib import admin
from django.urls import path
from .views import weather_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', weather_page, name='weather_page')
]
