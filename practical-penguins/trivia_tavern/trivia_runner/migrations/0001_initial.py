# Generated by Django 3.1 on 2020-08-09 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import trivia_runner.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trivia_builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveTriviaQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_code', models.CharField(default=trivia_runner.models.gen_session_code, editable=False, max_length=6, unique=True)),
                ('current_question_index', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(default='', max_length=24)),
                ('phone_number', models.CharField(max_length=12)),
                ('active_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia_runner.activetriviaquiz')),
            ],
        ),
        migrations.AddField(
            model_name='activetriviaquiz',
            name='players',
            field=models.ManyToManyField(related_name='quiz_players', to='trivia_runner.Player'),
        ),
        migrations.AddField(
            model_name='activetriviaquiz',
            name='session_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_master', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activetriviaquiz',
            name='trivia_quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia_builder.triviaquiz'),
        ),
    ]
