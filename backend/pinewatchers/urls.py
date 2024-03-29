from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views
from robots import views

router = DefaultRouter()
router.register(r"robots", views.RobotsViewSet, basename="robots")
router.register(
    r"locations", views.LocationFilterViewSet, basename="get_robot_locations"
)
router.register(
    r"telemetrics",
    views.GetTelemetricsViewSet,
    basename="get_robot_telemetries",
)
router.register(
    r"lastlocation",
    views.GetLatestLocationViewSet,
    basename="get_latest_location",
)
router.register(
    r"modifybrand",
    views.ModifyRobotBrandViewSet,
    basename="modify_robot_brand",
)
router.register(
    r"addclient", views.AddNewClientViewSet, basename="add_new_client"
)
router.register(
    r"detach",
    views.DetachCommunicationDeviceViewSet,
    basename="detach_communication_device",
)
router.register(
    r"attach",
    views.AttachCommunicationDeviceViewSet,
    basename="attach_communication_device",
)
router.register(
    r"deattach",
    views.DetachAttachCommunicationDeviceViewSet,
    basename="detach_attach_communication_device",
)
router.register(
    r"modifyrobot", views.ModifyRobotViewSet, basename="modify_specified_robot"
)
router.register(
    r"addcomm",
    views.AddCommunicationDeviceViewSet,
    basename="add_communication_device",
)
router.register(
    r"deleterobot", views.RemoveRobotViewSet, basename="delete_robot"
)
router.register(
    r"deletelocations",
    views.RemoveLocationViewSet,
    basename="delete_specified_locations",
)
router.register(
    r"settemperature",
    views.SetTempertatureViewSet,
    basename="change_temperature",
)
router.register(
    r"addclientformapi",
    views.CreateCompanyViewSet,
    basename="add_client_from_api",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robotsapp/", include("robots.urls")),
    path("authentication/", auth_views.obtain_auth_token)
] + router.urls
