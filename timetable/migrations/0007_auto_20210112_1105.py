# Generated by Django 3.1.4 on 2021-01-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0006_remove_timetable_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='course',
            field=models.CharField(choices=[('GES', 'GES'), ('CSC', 'CSC'), ('ECON', 'ECON')], max_length=50, null=True),
        ),
    ]
