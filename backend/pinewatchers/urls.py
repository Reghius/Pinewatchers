from django.contrib import admin
from django.urls import path, include
from robots import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'robots', views.RobotsViewSet, basename='robots')
router.register(r'locations', views.GetLocationsViewSet, basename='get_robot_locations')
router.register(r'telemetries', views.GetTelemetricsViewSet, basename='get_robot_telemetries')
router.register(r'lastlocation', views.GetLatestLocationViewSet, basename='get_latest_location')
router.register(r'modifybrand', views.ModifyRobotBrandViewSet, basename='modify_robot_brand')
router.register(r'addclient', views.AddNewClientViewSet, basename='add_new_client')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robotsapp/', include('robots.urls'))
] + router.urls
