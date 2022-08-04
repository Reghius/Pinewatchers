from django.contrib import admin
from django.urls import path, include
from robots import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'robots', views.RobotsViewSet, basename='robots')
router.register(r'robotsdata', views.RobotsDataViewSet, basename='robots_data')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robotsapp/', include('robots.urls'))
] + router.urls
