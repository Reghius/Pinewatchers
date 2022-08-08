# Generated by Django 3.2.15 on 2022-08-08 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0026_auto_20220808_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='robot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='robots.robot'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='robots.robotmanufacturer'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='robots.robottype'),
        ),
        migrations.AlterField(
            model_name='telemetry',
            name='robot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='robots.robot'),
        ),
    ]
