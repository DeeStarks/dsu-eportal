# Generated by Django 3.1.4 on 2021-01-17 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_department'),
        ('user_profile', '0008_auto_20210117_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourses',
            name='courses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]
