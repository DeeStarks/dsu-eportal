# Generated by Django 3.1.4 on 2021-01-05 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20210102_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='level',
            field=models.CharField(blank=True, choices=[('FRESHMAN', 'Freshman (100)'), ('SOPHOMORE', 'Sophomore (200)'), ('JUNIOR', 'Junior (300)'), ('SENIOR', 'Senior (400)'), ('M-POSTGRADUATE', 'Postgraduate (M.Sc)'), ('P-POSTGRADUATE', 'Postgraduate (Ph.D)')], max_length=200, null=True),
        ),
    ]
