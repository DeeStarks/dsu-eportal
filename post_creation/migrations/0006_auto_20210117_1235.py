# Generated by Django 3.1.4 on 2021-01-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_creation', '0005_auto_20201224_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.TextField(blank=True, null=True),
        ),
    ]
