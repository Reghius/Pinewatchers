from asyncore import read
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
    # owner = ClientSerializer()
    # type = RobotTypeSerialzer()
    owner = serializers.SlugRelatedField(read_only=True, slug_field='name')
    type = serializers.SlugRelatedField(read_only=True, slug_field='robot_type')

    class Meta:
        model = Robot
        fields = (
            'owner',
            'type'
        )
