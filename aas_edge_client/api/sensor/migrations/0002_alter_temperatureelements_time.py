# Generated by Django 4.2.5 on 2023-10-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperatureelements',
            name='Time',
            field=models.DateTimeField(),
        ),
    ]