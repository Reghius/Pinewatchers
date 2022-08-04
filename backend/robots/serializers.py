from asyncore import read
from rest_framework import serializers
from robots.models import Robot, Client, RobotType, RobotManufacturer


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


class RobotsSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    type = RobotTypeSerialzer()

    class Meta:
        model = Robot
        fields = (
            'owner',
            'type'
        )


class RobotsDataSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    type = RobotTypeSerialzer()
    manufacturer = ManufacturerSerializer()
    class Meta:
        model = Robot
        fields = '__all__'
