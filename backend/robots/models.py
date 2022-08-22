from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import Group


class Client(models.Model):
    name = models.CharField(max_length=200)
    krs_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)]
        )
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    street_number = models.CharField(max_length=100, blank=True)
    phone_numer = models.CharField(max_length=20, blank=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class RobotType(models.Model):
    class ChoiceField:
        wheeler = "4wheeler"
        amphibian = "amphibian"
        tracked = "tracked"
        flying = "flying"
        robot_type_choice = [
            (wheeler, "4 wheeler"),
            (amphibian, "amphibian"),
            (tracked, "tracked"),
            (flying, "flying"),
        ]

    robot_type = models.CharField(
        max_length=20,
        choices=ChoiceField.robot_type_choice,
        default="default",
    )

    def __str__(self):
        return f"{self.robot_type}"


class RobotManufacturer(models.Model):
    name = models.CharField(max_length=200)
    country_of_origin = models.CharField(max_length=100)
    hq_location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Robot(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(
        RobotManufacturer, on_delete=models.DO_NOTHING
    )
    serial_number = models.CharField(max_length=200)
    production_date = models.DateField()
    type = models.ForeignKey(RobotType, on_delete=models.DO_NOTHING)
    proprietor = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True)

    def __str__(self):
        return f"{self.name}"


class CommunicationDevice(models.Model):
    name = models.CharField(max_length=100, unique=True)
    x_size = models.FloatField()
    y_size = models.FloatField()
    z_size = models.FloatField()
    robot = models.OneToOneField(
        Robot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="communication_device",
    )

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    robot = models.ForeignKey(Robot, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.robot}"


class Telemetry(models.Model):
    robot = models.ForeignKey(Robot, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    pressure = models.FloatField()

    def __str__(self):
        return f"{self.robot}"


class RobotModificationHistory(models.Model):
    name = models.CharField(max_length=200, blank=True)
    owner = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    serial_number = models.CharField(max_length=200, blank=True)
    production_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name}"
