from tkinter import CASCADE
from django.db import models


class RobotType(models.Model):
    WHEELER = '4WEELER'
    AMPHIBIAN = 'AMPHIBIAN'
    TRACKED = 'TRACKED'
    FLYING = 'FLYING'
    ROBOT_TYPE_CHOICE = [
        (WHEELER, '4 wheeler'),
        (AMPHIBIAN, 'Amphibian'),
        (TRACKED, 'Tracked'),
        (FLYING, 'Flying'),
    ]
    robot_type = models.CharField(
        max_length=20,
        choices=ROBOT_TYPE_CHOICE,
        default=WHEELER,
    )

    def __str__(self):
        return f'{self.robot_type}'


class CommunicationDevice(models.Model):
    device_id = models.CharField(max_length=20)
    device_x_size = models.FloatField()
    device_y_size = models.FloatField()
    device_z_size = models.FloatField()

    def __str__(self):
        return f'{self.device_id}'


class Robot(models.Model):
    robot_name = models.CharField(max_length=20)
    robot_manufacturer = models.CharField(max_length=20)
    robot_serial_number = models.CharField(max_length=20)
    robot_production_date = models.DateField()
    robot_type = models.ForeignKey(RobotType, on_delete=models.CASCADE)
    communication_device_id = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.robot_name}'


class Location(models.Model):
    robot_name = models.ForeignKey(Robot, on_delete=models.CASCADE)
    communication_device_id = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Telemetry(models.Model):
    robot_name = models.ForeignKey(Robot, on_delete=models.CASCADE)
    communication_device_id = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    pressure = models.FloatField()
