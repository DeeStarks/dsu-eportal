# Generated by Django 3.1.4 on 2021-01-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0012_auto_20210123_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_result', models.BooleanField(default=False)),
            ],
        ),
    ]
