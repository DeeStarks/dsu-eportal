# Generated by Django 3.1.3 on 2020-12-17 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AddBook',
            new_name='Book',
        ),
    ]
