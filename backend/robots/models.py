from django.db import models


class RobotType(models.Model):
    WHEELER = '4W'
    AMPHIBIAN = 'AM'
    TRACKED = 'TR'
    FLYING = 'FL'
    ROBOT_TYPE_CHOICE = [
        (WHEELER, '4 wheeler'),
        (AMPHIBIAN, 'Amphibian'),
        (TRACKED, 'Tracked'),
        (FLYING, 'Flying'),
    ]
    robot_type = models.CharField(
        max_length=2,
        choices=ROBOT_TYPE_CHOICE,
        default=WHEELER,
    )


class CommunicationDevice(models.Model):
    device_id = models.CharField(max_length=20)
    device_x_size = models.FloatField()
    device_y_size = models.FloatField()
    device_z_size = models.FloatField()
