# Generated by Django 3.2.16 on 2023-05-26 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='user_token',
        ),
    ]
