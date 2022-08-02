from tracemalloc import start
from urllib.request import HTTPErrorProcessor
from xml.dom import ValidationErr
from django.forms import ValidationError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from robots.models import Client, Robot, Location, Telemetry, CommunicationDevice, RobotManufacturer


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

    if not robot_id or not start_date or not end_date:
        return HttpResponse('robot_id must be an integer and dates must be in YYYY-MM-DD format')

    try:
        location = Location.objects.filter(robot_name=robot_id, timestamp__range=[start_date, end_date])
    except ValueError:
        return HttpResponse('robot_id must be an integer')
    except ValidationError:
        return HttpResponse('start_date and end_date must me in YYYY-MM-DD format')

    if Robot.objects.filter(id=robot_id).exists():
        pass
    else:
        return HttpResponse('robot with specified id does not exist')

    result = []
    for data in location:
        aux = {
            'robot_name': data.robot_name.name,
            'latitude': data.latitude,
            'longitude': data.longitude
        }
        result.append(aux)

    return JsonResponse(result, safe=False)


def get_telemetry(request):
    robot_id = request.GET.get('robot_id', None)
    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)

    telemetry = Telemetry.objects.filter(robot_name=robot_id, timestamp__range=[start_date, end_date])
    result = []
    for data in telemetry:
        aux = {
            'robot_name': data.robot_name.name,
            'humidity': data.humidity,
            'temperature': data.temperature,
            'pressure': data.pressure
        }
        result.append(aux)

    return JsonResponse(result, safe=False)


def get_latest_location(request):
    result = []
    for aux in Robot.objects.all():
        try:
            data = aux.location_set.latest('timestamp')
            result.append({
                'robot_name': data.robot_name.name,
                'timestamp': data.timestamp,
                'latitude': data.latitude,
                'longitude': data.longitude
            })
        except Location.DoesNotExist:
            result.append({
                'robot_name': aux.name,
                'timestamp': 'No data',
                'latitude': 'No data',
                'longitude': 'No data'
            })

    return JsonResponse(result, safe=False)


def modify_robot_brand(request, robot_id):
    robot_data = get_object_or_404(Robot, id=robot_id)
    post_data = request.POST.get('manufacturer_id', None)
    if post_data.isnumeric() == True and len(post_data)>0 and RobotManufacturer.objects.filter(pk=post_data).exists():
        robot_data.manufacturer_id = post_data
        robot_data.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse('Wrong value')


def add_new_client(request):
    client_name = request.POST['name']
    krs_number = request.POST['KRS_number']
    if len(client_name)>0 and len(client_name)<50 and len(krs_number) == 10 and krs_number.isnumeric() == True:
        client = Client.objects.create(name=client_name, KRS_number=krs_number)
        client.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse('Name has to have at least one and no more then 50 signs. KRS has to have 10 numbers')
