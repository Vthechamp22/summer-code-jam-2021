# Generated by Django 3.0.8 on 2020-08-02 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_auto_20200802_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
