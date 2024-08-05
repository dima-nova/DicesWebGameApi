# Generated by Django 5.0.7 on 2024-07-31 18:44

import django.db.models.deletion
import game_rooms.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('id_code', game_rooms.fields.IdCodeField(max_length=6, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('max_players', models.IntegerField(default=2)),
                ('is_private', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, max_length=218)),
                ('is_started', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
                ('delete_at', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_rooms', to=settings.AUTH_USER_MODEL)),
                ('players_list', models.ManyToManyField(related_name='rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]