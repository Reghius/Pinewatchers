from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from robots.models import Robot, RobotModificationHistory


@receiver(post_save, sender=Robot, dispatch_uid="save_changes")
def save_changes(sender, instance, **kwargs):
    RobotModificationHistory.objects.create(
        name=instance.name,
        owner=instance.owner,
        manufacturer=instance.manufacturer,
        serial_number=instance.serial_number,
        production_date=instance.production_date,
        type=instance.type,
        modification_date=datetime.now()
        )
