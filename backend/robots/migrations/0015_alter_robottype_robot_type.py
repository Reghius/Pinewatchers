# Generated by Django 3.2.14 on 2022-07-21 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robots", "0014_auto_20220721_0726"),
    ]

    operations = [
        migrations.AlterField(
            model_name="robottype",
            name="robot_type",
            field=models.CharField(
                choices=[
                    ("4WEELER", "4 wheeler"),
                    ("AMPHIBIAN", "Amphibian"),
                    ("TRACKED", "Tracked"),
                    ("FLYING", "Flying"),
                ],
                default="default",
                max_length=20,
            ),
        ),
    ]
