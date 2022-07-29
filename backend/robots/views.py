from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
    sensor_id = request.GET.get('sensor_id', None)
    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)

    location = Location.objects.filter(communication_device_id=sensor_id, timestamp__range=[start_date, end_date])
    result = []
    for data in location:
        aux = {
            'communication_device_name': data.communication_device.name,
            'latitude': data.latitude,
            'longitude': data.longitude
        }
        result.append(aux)

    return JsonResponse(result, safe=False)


def get_telemetry(request):
    sensor_id = request.GET.get('sensor_id', None)
    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)

    telemetry = Telemetry.objects.filter(communication_device_id=sensor_id, timestamp__range=[start_date, end_date])
    result = []
    for data in telemetry:
        aux = {
            'communication_device_name': data.communication_device.name,
            'humidity': data.humidity,
            'temperature': data.temperature,
            'pressure': data.pressure
        }
        result.append(aux)

    return JsonResponse(result, safe=False)


def get_latest_location(request):
    result = []
    try:
        for aux in CommunicationDevice.objects.all():
            data = aux.location_set.latest('timestamp')
            result.append({
                'communication_device': data.communication_device.name,
                'timestamp': data.timestamp,
                'latitude': data.latitude,
                'longitude': data.longitude
            })
    except:
        pass
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
