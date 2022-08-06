from rest_framework import serializers
from robots.models import Robot, Client, RobotType, RobotManufacturer, Location, Telemetry, CommunicationDevice


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ('name',)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name',)


class RobotTypeSerialzer(serializers.ModelSerializer):
    class Meta:
        model = RobotType
        fields = ('robot_type',)


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotManufacturer
        fields = ('name',)


class RobotsDataSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    type = RobotTypeSerialzer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Robot
        fields = '__all__'


class GetRobotLocations(serializers.ModelSerializer):
    robot = RobotSerializer()

    class Meta:
        model = Location
        fields = (
            'robot',
            'latitude',
            'longitude'
        )


class GetRobotTelemetrics(serializers.ModelSerializer):
    robot = RobotSerializer()

    class Meta:
        model = Telemetry
        fields = (
            'robot',
            'humidity',
            'temperature',
            'pressure'
        )


class GetLastLocationSerializer(serializers.ModelSerializer):
    robot = RobotSerializer()

    class Meta:
        model = Location
        fields = (
            'robot',
            'timestamp',
            'latitude',
            'longitude'
        )


class ModifyRobotBrand(serializers.ModelSerializer):

    class Meta:
        model = Robot
        fields = ('manufacturer',)



class AddNewClient(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('name', 'krs_number')


class DetachCommunicationSerializer(serializers.ModelSerializer):
    robot = RobotSerializer

    class Meta:
        model = CommunicationDevice
        fields = ('id', 'robot')


class AttachCommunicationSerializer(serializers.ModelSerializer):
    robot = RobotSerializer

    class Meta:
        model = CommunicationDevice
        fields = ('id', 'robot')
