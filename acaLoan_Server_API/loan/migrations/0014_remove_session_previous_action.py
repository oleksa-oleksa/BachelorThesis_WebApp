# Generated by Django 3.0.5 on 2020-05-25 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0013_session_previous_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='previous_action',
        ),
    ]