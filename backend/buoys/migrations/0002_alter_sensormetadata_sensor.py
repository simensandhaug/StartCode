# Generated by Django 4.1.2 on 2022-10-23 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buoys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensormetadata',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_metadata', to='buoys.sensor'),
        ),
    ]
