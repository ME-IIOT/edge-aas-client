# Generated by Django 4.2.5 on 2023-10-04 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interfaces', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interface',
            name='LinkLocalIPv6Address',
        ),
        migrations.RemoveField(
            model_name='interface',
            name='NetworkMask',
        ),
        migrations.AlterField(
            model_name='interface',
            name='Name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]