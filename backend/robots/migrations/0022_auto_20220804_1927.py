# Generated by Django 3.2.15 on 2022-08-04 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0021_auto_20220802_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='robot_name',
            new_name='robot',
        ),
        migrations.RenameField(
            model_name='telemetry',
            old_name='robot_name',
            new_name='robot',
        ),
    ]
