from django.db import models
from django.forms import ChoiceField


class Client(models.Model):
    name = models.CharField(max_length=200)
    krs_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    street_number = models.CharField(max_length=100, blank=True)
    phone_numer = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.name}'


class RobotType(models.Model):
    class ChoiceField():
        wheeler = '4wheeler'
        amphibian = 'amphibian'
        tracked = 'tracked'
        flying = 'flying'
        robot_type_choice = [
            (wheeler, '4 wheeler'),
            (amphibian, 'amphibian'),
            (tracked, 'tracked'),
            (flying, 'flying'),
        ]
    robot_type = models.CharField(
        max_length=20,
        choices=ChoiceField.robot_type_choice,
        default='default',
    )

    def __str__(self):
        return f'{self.robot_type}'


class RobotManufacturer(models.Model):
    name = models.CharField(max_length=200)
    country_of_origin = models.CharField(max_length=100)
    hq_location = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class CommunicationDevice(models.Model):
    name = models.CharField(max_length=100)
    x_size = models.FloatField()
    y_size = models.FloatField()
    z_size = models.FloatField()
    is_faulty = models.BooleanField()

    def __str__(self):
        return f'{self.name}'


class Robot(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(RobotManufacturer, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=200)
    production_date = models.DateField()
    type = models.ForeignKey(RobotType, on_delete=models.CASCADE)
    communication_device = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Location(models.Model):
    communication_device = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Telemetry(models.Model):
    communication_device = models.ForeignKey(CommunicationDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    pressure = models.FloatField()
