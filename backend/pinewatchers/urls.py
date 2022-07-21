from django.contrib import admin
from django.urls import path, include
from robots import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robotsapp/', include('robots.urls'))
]
