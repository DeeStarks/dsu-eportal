# Generated by Django 3.1.4 on 2021-01-22 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0002_studentgrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='continousassessment',
            name='gp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]