# Generated by Django 3.1.4 on 2021-01-17 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_department'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0007_auto_20210117_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourses',
            name='courses',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AlterField(
            model_name='studentcourses',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
