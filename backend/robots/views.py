from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from robots.models import Client, RobotManufacturer, RobotType, CommunicationDevice, Robot, Location, Telemetry


def get_robots(request):
    temp = list(Robot.objects.values('type', 'owner'))
    return JsonResponse(temp, safe=False)


def get_robots_data(request):
    data = list(Robot.objects.values())
    return JsonResponse(data, safe=False)


def get_robot_data(request, robot_id):
    data = get_object_or_404(Robot, id=robot_id)
    aux = {
        'name': data.name,
        'owner': data.owner.name,
        'manufacturer': data.manufacturer,
        'serial_number': data.serial_number,
        'production_date': data.production_date,
        'robot_type': data.type.robot_type,
        'communication_device_name': data.communication_device_name.name
    }

    return JsonResponse(aux, safe=False)
