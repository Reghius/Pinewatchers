# Generated by Django 3.2.14 on 2022-07-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robots", "0016_auto_20220727_0957"),
    ]

    operations = [
        migrations.AddField(
            model_name="communicationdevice",
            name="is_faulty",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
