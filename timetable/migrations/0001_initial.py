# Generated by Django 3.1.4 on 2021-01-08 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('ACADEMIC_CALENDAR', 'Academic Calendar'), ('EXAM_TIMETABLE', 'Exam Timetable')], max_length=100, null=True)),
                ('session', models.CharField(choices=[('YEAR_1', '2020/2021 Session'), ('YEAR_2', '2021/2022 Session')], max_length=50, null=True)),
                ('semester', models.CharField(choices=[('SEMESETER_1', 'First Semester'), ('SEMESETER_2', 'Second Semester')], max_length=50, null=True)),
                ('courses', models.CharField(choices=[('CSC', 'CSC'), ('GES', 'GES'), ('ECON', 'ECON')], max_length=50, null=True)),
            ],
        ),
    ]