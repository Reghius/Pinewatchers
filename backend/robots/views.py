from tracemalloc import start
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from robots.models import Client, RobotManufacturer, RobotType, CommunicationDevice, Robot, Location, Telemetry


def get_robots(request):
    data = Robot.objects.all().select_related('owner', 'type')
    result = []
    for robot in data:
        aux = {
            'owner': robot.owner.name,
            'robot_type': robot.type.robot_type
        }
        result.append(aux)

    return JsonResponse(result, safe=False)


def get_robots_data(request):
    data = Robot.objects.all().select_related('owner', 'manufacturer', 'type', 'communication_device_name')
    result = []
    for robot in data:
        aux = {
        'id': robot.id,
        'name': robot.name,
        'owner': robot.owner.name,
        'manufacturer': robot.manufacturer.name,
        'serial_number': robot.serial_number,
        'production_date': robot.production_date,
        'robot_type': robot.type.robot_type,
        'communication_device_name': robot.communication_device_name.name
        }
        result.append(aux)
    
    return JsonResponse(result, safe=False)


def get_robot_data(request, robot_id):
    data = get_object_or_404(Robot, id=robot_id)
    aux = {
        'name': data.name,
        'owner': data.owner.name,
        'manufacturer': data.manufacturer.name,
        'serial_number': data.serial_number,
        'production_date': data.production_date,
        'robot_type': data.type.robot_type,
        'communication_device_name': data.communication_device_name.name
    }

    return JsonResponse(aux, safe=False)


def get_location(request):
    robot_id = request.GET.get('robot_id', None)
    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)

    location = Location.objects.filter(robot_object_id__id=robot_id, timestamp__range=[start_date, end_date])
    result = []
    for data in location:
        aux = {
            'robot': data.robot_object.pk,
            'communication_device_name': data.communication_device_name.name,
            'latitude': data.latitude,
            'longitude': data.longitude
        }
        result.append(aux)

    return JsonResponse(result, safe=False)


def get_telemetry(request):
    robot_id = request.GET.get('robot_id', None)
    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)

    telemetry = Telemetry.objects.filter(robot_object_id__id=robot_id, timestamp__range=[start_date, end_date])
    result = []
    for data in telemetry:
        aux = {
            'robot': data.robot_object.pk,
            'communication_device_name': data.communication_device_name.name,
            'humidity': data.humidity,
            'temperature': data.temperature,
            'pressure': data.pressure
        }
        result.append(aux)

    return JsonResponse(result, safe=False)
