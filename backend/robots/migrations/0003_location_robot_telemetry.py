# Generated by Django 3.2.14 on 2022-07-13 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0002_auto_20220713_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robot_name', models.CharField(max_length=20)),
                ('robot_manufacturer', models.CharField(max_length=20)),
                ('robot_serial_number', models.CharField(max_length=20)),
                ('robot_production_date', models.DateField()),
                ('communication_device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.communicationdevice')),
                ('robot_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.robottype')),
            ],
        ),
        migrations.CreateModel(
            name='Telemetry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('humidity', models.FloatField()),
                ('temperature', models.FloatField()),
                ('pressure', models.FloatField()),
                ('communication_device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.communicationdevice')),
                ('robot_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.robot')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('communication_device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.communicationdevice')),
                ('robot_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robots.robot')),
            ],
        ),
    ]