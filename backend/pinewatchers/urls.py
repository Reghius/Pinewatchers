from django.contrib import admin
from django.urls import path, include
from robots import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'robots', views.RobotsViewSet, basename='robots')
router.register(r'locations', views.LocationFilterViewSet, basename='get_robot_locations')
router.register(r'telemetrics', views.GetTelemetricsViewSet, basename='get_robot_telemetries')
router.register(r'lastlocation', views.GetLatestLocationViewSet, basename='get_latest_location')
router.register(r'modifybrand', views.ModifyRobotBrandViewSet, basename='modify_robot_brand')
router.register(r'addclient', views.AddNewClientViewSet, basename='add_new_client')
router.register(r'detach', views.DetachCommunicationDeviceViewSet, basename='detach_communication_device')
router.register(r'attach', views.AttachCommunicationDeviceViewSet, basename='attach_communication_device')
router.register(r'deattach', views.DetachAttachCommunicationDeviceViewSet, basename='detach_attach_communication_device')
router.register(r'modifyrobot', views.ModifyRobotViewSet, basename='modify_specified_robot')
router.register(r'addcomm', views.AddCommunicationDeviceViewSet, basename='add_communication_device')
router.register(r'deleterobot', views.RemoveRobotViewSet, basename='delete_robot')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robotsapp/', include('robots.urls')),
] + router.urls
