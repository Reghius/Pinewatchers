# Generated by Django 3.2.14 on 2022-07-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0003_location_robot_telemetry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robottype',
            name='robot_type',
            field=models.CharField(choices=[('4WEELER', '4 wheeler'), ('AMPHIBIAN', 'Amphibian'), ('TRACKED', 'Tracked'), ('FLYING', 'Flying')], default='4WEELER', max_length=20),
        ),
    ]