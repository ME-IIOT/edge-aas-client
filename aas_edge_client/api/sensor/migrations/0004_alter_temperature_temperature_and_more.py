# Generated by Django 4.2.5 on 2023-10-10 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0003_rename_temperature_sensors_sensors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='Temperature',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Temperature', to='sensor.temperatureelements'),
        ),
        migrations.AlterField(
            model_name='temperatureelements',
            name='Time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]