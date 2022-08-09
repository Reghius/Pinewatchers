# Generated by Django 3.2.15 on 2022-08-08 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robots", "0027_auto_20220808_0909"),
    ]

    operations = [
        migrations.CreateModel(
            name="RobotModificationHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("owner", models.CharField(max_length=200)),
                ("manufacturer", models.CharField(max_length=200)),
                ("serial_number", models.CharField(max_length=200)),
                ("production_date", models.DateField()),
                ("type", models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name="location",
            name="robot",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="robots.robot",
            ),
        ),
        migrations.AlterField(
            model_name="telemetry",
            name="robot",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="robots.robot",
            ),
        ),
    ]
