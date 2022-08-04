from rest_framework import serializers
from robots.models import Robot, Client, RobotType


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name',)


class RobotTypeSerialzer(serializers.ModelSerializer):
    class Meta:
        model = RobotType
        fields = ('robot_type',)


class RobotsSerializer(serializers.ModelSerializer):
    owner = ClientSerializer()
    type = RobotTypeSerialzer()

    class Meta:
        model = Robot
        fields = (
            'owner',
            'type'
        )
