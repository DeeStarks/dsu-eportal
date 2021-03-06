# Generated by Django 3.1.4 on 2021-01-22 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(blank=True, max_length=100, null=True)),
                ('semester', models.CharField(blank=True, max_length=100, null=True)),
                ('tcu', models.IntegerField(blank=True, null=True)),
                ('gpa', models.IntegerField(blank=True, null=True)),
                ('cgpa', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
