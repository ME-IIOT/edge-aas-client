# Generated by Django 4.2.5 on 2023-10-10 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_alter_temperatureelements_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensors',
            old_name='Temperature',
            new_name='Sensors',
        ),
    ]
