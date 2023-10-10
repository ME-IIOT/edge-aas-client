# Generated by Django 4.2.5 on 2023-10-10 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemperatureElements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('Value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Temperature', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temperature', to='sensor.temperatureelements')),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Temperature', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sensor.temperature')),
            ],
        ),
    ]