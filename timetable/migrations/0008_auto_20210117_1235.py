# Generated by Django 3.1.4 on 2021-01-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_auto_20210112_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='course',
            field=models.CharField(choices=[], max_length=50, null=True),
        ),
    ]
