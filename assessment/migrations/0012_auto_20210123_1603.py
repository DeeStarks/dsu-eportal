# Generated by Django 3.1.4 on 2021-01-23 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_department'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessment', '0011_continousassessment_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='continousassessment',
            name='carryover',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CarryOver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
