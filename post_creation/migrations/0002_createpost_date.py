# Generated by Django 3.1.3 on 2020-12-16 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_creation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='createpost',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]