# Generated by Django 3.1.4 on 2021-01-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0010_uploadedscoresheets'),
    ]

    operations = [
        migrations.AddField(
            model_name='continousassessment',
            name='level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
