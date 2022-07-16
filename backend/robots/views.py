from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from robots.models import Client, RobotManufacturer, RobotType, CommunicationDevice, Robot, Location, Telemetry


def get_robots(request):
    temp = list(Robot.objects.values('type', 'owner'))
    return JsonResponse(temp, safe=False)


def get_robots_data(request):
    data = list(Robot.objects.values())
    return JsonResponse(data, safe=False)