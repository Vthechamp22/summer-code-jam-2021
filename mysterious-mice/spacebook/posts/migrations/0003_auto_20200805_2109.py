# Generated by Django 3.0.8 on 2020-08-06 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200801_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]