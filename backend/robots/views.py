from datetime import datetime
import requests
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from robots.filters import LocationFilter, RobotFilter, TelemetryFilter
from robots.models import (
    Client,
    CommunicationDevice,
    Location,
    Robot,
    Telemetry,
)
from robots.paginations import RobotsPagination
from robots.serializers import (
    AddCommunicationDeviceSerializer,
    AddNewClient,
    AttachCommunicationSerializer,
    DeleteLocationsSerializer,
    DetachCommunicationSerializer,
    GetLastLocationSerializer,
    GetRobotLocations,
    GetRobotTelemetrics,
    ModifyRobotBrand,
    ModifyRobotSerializer,
    RobotsDataSerializer,
)


class RobotsViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = RobotsDataSerializer
    pagination_class = RobotsPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RobotFilter

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = Robot.objects.filter(proprietor__in=group)
        return queryset


class LocationFilterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GetRobotLocations
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationFilter

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = Location.objects.filter(robot__proprietor__in=group)
        return queryset


class GetTelemetricsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GetRobotTelemetrics
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TelemetryFilter

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = Telemetry.objects.filter(robot__proprietor__in=group)
        return queryset


class GetLatestLocationViewSet(viewsets.ModelViewSet):
    serializer_class = GetLastLocationSerializer

    def get_queryset(self):
        group = self.request.user.groups.all()
        location = Location.objects.order_by("robot", "-timestamp").distinct(
            "robot"
        ).filter(robot__proprietor__in=group)
        return location


class ModifyRobotBrandViewSet(
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = ModifyRobotBrand

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = Robot.objects.filter(proprietor__in=group)
        return queryset


class AddNewClientViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = AddNewClient


class DetachCommunicationDeviceViewSet(
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = DetachCommunicationSerializer

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = CommunicationDevice.objects.filter(
            robot__proprietor__in=group
            )
        return queryset


class AttachCommunicationDeviceViewSet(
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = AttachCommunicationSerializer

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = CommunicationDevice.objects.filter(
            robot__proprietor__in=group
        )
        return queryset


class DetachAttachCommunicationDeviceViewSet(
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    # queryset = CommunicationDevice.objects.all()
    serializer_class = DetachCommunicationSerializer

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = CommunicationDevice.objects.filter(
            robot__proprietor__in=group
        )
        return queryset

    def update(self, request, *args, **kwargs):
        from_device = self.get_object()
        to_device = request.GET.get("to")
        new = CommunicationDevice.objects.get(id=to_device)
        new.robot = from_device.robot
        from_device.robot = None
        from_device.save()
        new.save()


class ModifyRobotViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = ModifyRobotSerializer

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = Robot.objects.filter(
            proprietor__in=group
        )
        return queryset


class AddCommunicationDeviceViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = CommunicationDevice.objects.all()
    serializer_class = AddCommunicationDeviceSerializer


class RemoveRobotViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RobotsDataSerializer

    def get_queryset(self):
        group = self.request.user.groups.all()
        queryset = Robot.objects.filter(
            proprietor__in=group
        )
        return queryset


class RemoveLocationViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Robot.objects.all()
    serializer_class = DeleteLocationsSerializer

    def destroy(self, request, *args, **kwargs):
        group = self.request.user.groups.all()
        device = self.get_object()
        date = request.GET.get("date")
        Location.objects.filter(
            robot__proprietor__in=group,
            robot=device,
            timestamp__date=date
        ).delete()


class SetTempertatureViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Robot.objects.all()
    serializer_class = DeleteLocationsSerializer

    def update(self, request, *args, **kwargs):
        group = self.request.user.groups.all()
        device = self.get_object()
        extra_device = request.GET.get("id")
        new_temperature = request.GET.get("temperature")
        date = request.GET.get("date")
        Telemetry.objects.filter(
            robot__proprietor__in=group,
            robot=device, timestamp__date=date
        ).update(temperature=new_temperature)
        Telemetry.objects.filter(
            robot__proprietor__in=group,
            robot=extra_device,
            timestamp__date=date
        ).update(temperature=new_temperature)


class CreateCompanyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = AddNewClient

    def create(self, request, *args, **kwargs):
        nip = request.GET.get("nip")
        data = requests.get(
            f"https://wl-api.mf.gov.pl/api/search/nip/{nip}"
            f"/?date={str(datetime.date(datetime.now()))}"
        )
        jsonResponse = data.json()
        name = jsonResponse["result"]["subject"]["name"]
        krs = jsonResponse["result"]["subject"]["krs"]
        Client.objects.create(name=name, krs_number=krs)


# def get_robots(request):
#     data = Robot.objects.all().select_related("owner", "type")
#     result = []
#     for robot in data:
#         aux = {"owner": robot.owner.name,
#  "robot_type": robot.type.robot_type}
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_robots_data(request):
#     data = Robot.objects.all().select_related("owner",
#  "manufacturer", "type")
#     result = []
#     for robot in data:
#         aux = {
#             "id": robot.id,
#             "name": robot.name,
#             "owner": robot.owner.name,
#             "manufacturer": robot.manufacturer.name,
#             "serial_number": robot.serial_number,
#             "production_date": robot.production_date,
#             "robot_type": robot.type.robot_type,
#         }
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_robot_data(request, robot_id):
#     data = get_object_or_404(Robot, id=robot_id)
#     aux = {
#         "name": data.name,
#         "owner": data.owner.name,
#         "manufacturer": data.manufacturer.name,
#         "serial_number": data.serial_number,
#         "production_date": data.production_date,
#         "robot_type": data.type.robot_type,
#     }

#     return JsonResponse(aux, safe=False)


# def get_location(request):
#     robot_id = request.GET.get("robot_id", None)
#     start_date = request.GET.get("start", None)
#     end_date = request.GET.get("end", None)

#     if not robot_id or not start_date or not end_date:
#         return HttpResponse(
#             "robot_id must be an integer and
#  dates must be in YYYY-MM-DD format"
#         )

#     try:
#         location = Location.objects.filter(
#             robot_name=robot_id, timestamp__range=[start_date, end_date]
#         )
#     except ValueError:
#         return HttpResponse("robot_id must be an integer")
#     except ValidationError:
#         return HttpResponse(
#             "start_date and end_date must me in YYYY-MM-DD format"
#         )

#     if Robot.objects.filter(id=robot_id).exists():
#         pass
#     else:
#         return HttpResponse("robot with specified id does not exist")

#     result = []
#     for data in location:
#         aux = {
#             "robot_name": data.robot_name.name,
#             "latitude": data.latitude,
#             "longitude": data.longitude,
#         }
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_telemetry(request):
#     robot_id = request.GET.get("robot_id", None)
#     start_date = request.GET.get("start", None)
#     end_date = request.GET.get("end", None)

#     if not robot_id or not start_date or not end_date:
#         return HttpResponse(
#             "robot_id must be an integer and dates must
#  be in YYYY-MM-DD format"
#         )

#     try:
#         telemetry = Telemetry.objects.filter(
#             robot_name=robot_id, timestamp__range=[start_date, end_date]
#         )
#     except ValueError:
#         return HttpResponse("robot_id must be an integer")
#     except ValidationError:
#         return HttpResponse(
#             "start_date and end_date must me in YYYY-MM-DD format"
#         )

#     if Robot.objects.filter(id=robot_id).exists():
#         pass
#     else:
#         return HttpResponse("robot with specified id does not exist")

#     result = []
#     for data in telemetry:
#         aux = {
#             "robot_name": data.robot_name.name,
#             "humidity": data.humidity,
#             "temperature": data.temperature,
#             "pressure": data.pressure,
#         }
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_latest_location(request):
#     result = []
#     for aux in Robot.objects.all():
#         try:
#             data = aux.location_set.latest("timestamp")
#             result.append(
#                 {
#                     "robot_name": data.robot_name.name,
#                     "timestamp": data.timestamp,
#                     "latitude": data.latitude,
#                     "longitude": data.longitude,
#                 }
#             )
#         except Location.DoesNotExist:
#             result.append(
#                 {
#                     "robot_name": aux.name,
#                     "timestamp": "No data",
#                     "latitude": "No data",
#                     "longitude": "No data",
#                 }
#             )

#     return JsonResponse(result, safe=False)


# def modify_robot_brand(request, robot_id):
#     robot_data = get_object_or_404(Robot, id=robot_id)
#     post_data = request.POST.get("manufacturer_id", None)
#     try:
#         if (
#             post_data.isnumeric() == True
#             and len(post_data) > 0
#             and RobotManufacturer.objects.filter(pk=post_data).exists()
#         ):
#             robot_data.manufacturer_id = post_data
#             robot_data.save()
#             return HttpResponse("Brand modified successfully")
#         else:
#             return HttpResponse("Given value does not exist")
#     except AttributeError:
#         return HttpResponse("Key is not filled in properly")


# def add_new_client(request):
#     try:
#         client_name = request.POST["name"]
#         krs_number = request.POST["krs_number"]
#     except MultiValueDictKeyError:
#         return HttpResponse("Key is not filled in properly")
#     if (
#         len(client_name) > 0
#         and len(client_name) < 50
#         and len(krs_number) == 10
#         and krs_number.isnumeric() == True
#     ):
#         client = Client.objects.create(name=client_name,
# krs_number=krs_number)
#         client.save()
#         return HttpResponse("Client added succesfully")
#     else:
#         return HttpResponse(
#             "Name has to have at least one and no more then 200 signs.
#  KRS has to have 10 numbers"
#         )
