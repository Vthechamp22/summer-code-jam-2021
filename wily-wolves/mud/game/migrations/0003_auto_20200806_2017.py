# Generated by Django 3.0.3 on 2020-08-07 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20200805_1214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='location_id',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='user_id',
            new_name='user',
        ),
    ]