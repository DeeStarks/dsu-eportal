# Generated by Django 3.1.4 on 2021-01-02 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_images/'),
        )
    ]