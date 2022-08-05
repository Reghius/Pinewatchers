from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from robots.serializers import RobotsSerializer, RobotsDataSerializer, GetRobotLocations, GetRobotTelemetrics, GetLastLocation, ModifyRobotBrand, AddNewClient
from robots.models import Client, Robot, Location, Telemetry, RobotManufacturer
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response


class RobotsViewSet(viewsets.ModelViewSet, ListModelMixin):
    queryset = Robot.objects.all()
    serializer_class = RobotsSerializer


class RobotsDataViewSet(viewsets.ModelViewSet, ListModelMixin):
    queryset = Robot.objects.all()
    serializer_class = RobotsDataSerializer

    def retrieve(self, request, pk=None):
        robot = get_object_or_404(Robot, pk=pk)
        serializer = RobotsDataSerializer(robot)
        return Response(serializer.data)


class GetLocationsViewSet(viewsets.ModelViewSet, ListModelMixin):
    serializer_class = GetRobotLocations

    def get_queryset(self):
        queryset = Location.objects.all()
        robot_id = self.request.query_params.get('robot_id')
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        if robot_id and start_date and end_date is not None:
            queryset = queryset.filter(robot_name=robot_id, timestamp__range=[start_date, end_date])
        return queryset


class GetTelemetricsViewSet(viewsets.ModelViewSet, ListModelMixin):
    serializer_class = GetRobotTelemetrics

    def get_queryset(self):
        queryset = Telemetry.objects.all()
        robot_id = self.request.query_params.get('robot_id')
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        if robot_id and start_date and end_date is not None:
            queryset = queryset.filter(robot_name=robot_id, timestamp__range=[start_date, end_date])
        return queryset


class GetLatestLocationViewSet(viewsets.ModelViewSet, ListModelMixin):
    serializer_class = GetLastLocation

    def get_queryset(self):
        location = Location.objects.order_by('robot', '-timestamp').distinct('robot')
        return location


class ModifyRobotBrandViewSet(viewsets.ModelViewSet, ListModelMixin):
    queryset = Robot.objects.all()
    serializer_class = ModifyRobotBrand

    def patch(self, request):
        robot = Robot.objects.get()
        data = request.data
        robot.manufacturer = data.get('manufacturer')
        robot.save()


class AddNewClient(viewsets.ModelViewSet, ListModelMixin):
    queryset = Client.objects.all()
    serializer_class = AddNewClient

    def create(self, request):
        client_data = request.data
        new_client = Client.objects.create(name=client_data['name'], krs_number=client_data['krs_number'])
        new_client.save()
        return HttpResponse('Client added')
        # serializer = AddNewClient(new_client)
        # return Response(serializer.data)


def add_new_client(request):
    try:
        client_name = request.POST['name']
        krs_number = request.POST['krs_number']
    except MultiValueDictKeyError:
        return HttpResponse('Key is not filled in properly')
    if len(client_name)>0 and len(client_name)<50 and len(krs_number) == 10 and krs_number.isnumeric() == True:
        client = Client.objects.create(name=client_name, krs_number=krs_number)
        client.save()
        return HttpResponse('Client added succesfully')
    else:
        return HttpResponse('Name has to have at least one and no more then 200 signs. KRS has to have 10 numbers')


# def get_robots(request):
#     data = Robot.objects.all().select_related('owner', 'type')
#     result = []
#     for robot in data:
#         aux = {
#             'owner': robot.owner.name,
#             'robot_type': robot.type.robot_type
#         }
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_robots_data(request):
#     data = Robot.objects.all().select_related('owner', 'manufacturer', 'type')
#     result = []
#     for robot in data:
#         aux = {
#         'id': robot.id,
#         'name': robot.name,
#         'owner': robot.owner.name,
#         'manufacturer': robot.manufacturer.name,
#         'serial_number': robot.serial_number,
#         'production_date': robot.production_date,
#         'robot_type': robot.type.robot_type,
#         }
#         result.append(aux)
    
#     return JsonResponse(result, safe=False)


# def get_robot_data(request, robot_id):
#     data = get_object_or_404(Robot, id=robot_id)
#     aux = {
#         'name': data.name,
#         'owner': data.owner.name,
#         'manufacturer': data.manufacturer.name,
#         'serial_number': data.serial_number,
#         'production_date': data.production_date,
#         'robot_type': data.type.robot_type,
#     }

#     return JsonResponse(aux, safe=False)


# def get_location(request):
#     robot_id = request.GET.get('robot_id', None)
#     start_date = request.GET.get('start', None)
#     end_date = request.GET.get('end', None)

#     if not robot_id or not start_date or not end_date:
#         return HttpResponse('robot_id must be an integer and dates must be in YYYY-MM-DD format')

#     try:
#         location = Location.objects.filter(robot_name=robot_id, timestamp__range=[start_date, end_date])
#     except ValueError:
#         return HttpResponse('robot_id must be an integer')
#     except ValidationError:
#         return HttpResponse('start_date and end_date must me in YYYY-MM-DD format')

#     if Robot.objects.filter(id=robot_id).exists():
#         pass
#     else:
#         return HttpResponse('robot with specified id does not exist')

#     result = []
#     for data in location:
#         aux = {
#             'robot_name': data.robot_name.name,
#             'latitude': data.latitude,
#             'longitude': data.longitude
#         }
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_telemetry(request):
#     robot_id = request.GET.get('robot_id', None)
#     start_date = request.GET.get('start', None)
#     end_date = request.GET.get('end', None)

#     if not robot_id or not start_date or not end_date:
#         return HttpResponse('robot_id must be an integer and dates must be in YYYY-MM-DD format')

#     try:
#         telemetry = Telemetry.objects.filter(robot_name=robot_id, timestamp__range=[start_date, end_date])
#     except ValueError:
#         return HttpResponse('robot_id must be an integer')
#     except ValidationError:
#         return HttpResponse('start_date and end_date must me in YYYY-MM-DD format')

#     if Robot.objects.filter(id=robot_id).exists():
#         pass
#     else:
#         return HttpResponse('robot with specified id does not exist')

#     result = []
#     for data in telemetry:
#         aux = {
#             'robot_name': data.robot_name.name,
#             'humidity': data.humidity,
#             'temperature': data.temperature,
#             'pressure': data.pressure
#         }
#         result.append(aux)

#     return JsonResponse(result, safe=False)


# def get_latest_location(request):
#     result = []
#     for aux in Robot.objects.all():
#         try:
#             data = aux.location_set.latest('timestamp')
#             result.append({
#                 'robot_name': data.robot_name.name,
#                 'timestamp': data.timestamp,
#                 'latitude': data.latitude,
#                 'longitude': data.longitude
#             })
#         except Location.DoesNotExist:
#             result.append({
#                 'robot_name': aux.name,
#                 'timestamp': 'No data',
#                 'latitude': 'No data',
#                 'longitude': 'No data'
#             })

#     return JsonResponse(result, safe=False)


# def modify_robot_brand(request, robot_id):
#     robot_data = get_object_or_404(Robot, id=robot_id)
#     post_data = request.POST.get('manufacturer_id', None)
#     try:
#         if post_data.isnumeric() == True and len(post_data)>0 and RobotManufacturer.objects.filter(pk=post_data).exists():
#             robot_data.manufacturer_id = post_data
#             robot_data.save()
#             return HttpResponse('Brand modified successfully')
#         else:
#             return HttpResponse('Given value does not exist')
#     except AttributeError:
#         return HttpResponse('Key is not filled in properly')
