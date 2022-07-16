from tkinter import CASCADE
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=20)
    KRS_number = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'


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


class RobotManufacturer(models.Model):
    name = models.CharField(max_length=20)
    country_of_origin = models.CharField(max_length=20)
    HQ_location = models.CharField(max_length=20)
    robot_types = models.CharField(max_length=20, choices=RobotType.ROBOT_TYPE_CHOICE)

    def __str__(self):
        return f'{self.name}'


class CommunicationDevice(models.Model):
    name = models.CharField(max_length=20)
    x_size = models.FloatField()
    y_size = models.FloatField()
    z_size = models.FloatField()

    def __str__(self):
        return f'{self.name}'


class Robot(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(RobotManufacturer, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=20)
    production_date = models.DateField()
    type = models.ForeignKey(RobotType, on_delete=models.CASCADE)
    communication_device_name = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Location(models.Model):
    robot_name = models.ForeignKey(Robot, on_delete=models.CASCADE)
    communication_device_name = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Telemetry(models.Model):
    robot_name = models.ForeignKey(Robot, on_delete=models.CASCADE)
    communication_device_name = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    pressure = models.FloatField()
