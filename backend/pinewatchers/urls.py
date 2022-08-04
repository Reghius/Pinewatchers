from django.contrib import admin
from django.urls import path, include
from robots import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'robots', views.RobotsViewSet, basename='robots')
router.register(r'robotsdata', views.RobotsDataViewSet, basename='robots_data')
router.register(r'locations', views.GetLocationsViewSet, basename='get_robot_locations')
router.register(r'telemetries', views.GetTelemetricsViewSet, basename='get_robot_telemetries')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robotsapp/', include('robots.urls'))
] + router.urls
