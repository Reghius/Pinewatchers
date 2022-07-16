from django.contrib import admin
from django.urls import path
from robots import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots/', views.get_robots, name='robots'),
    path('robots/data/', views.get_robots_data, name='robots data')
]
