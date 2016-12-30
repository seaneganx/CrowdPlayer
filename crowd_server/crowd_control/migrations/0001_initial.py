# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-30 05:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('spotify_id', models.CharField(max_length=64, unique=True, verbose_name='Spotify user ID')),
                ('spotify_access_token', models.CharField(max_length=255, unique=True, verbose_name='Spotify Web API Access Token')),
                ('spotify_access_expiry', models.DateTimeField(verbose_name='Spotify Access Token Expiry Date')),
                ('spotify_refresh_token', models.CharField(max_length=255, unique=True, verbose_name='Spotify Web API Refresh Token')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_name', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Room Name')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crowd_control.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_id', models.CharField(max_length=64, verbose_name='Spotify track ID')),
                ('artist_name', models.CharField(max_length=64, verbose_name='Artist Name')),
                ('track_name', models.CharField(max_length=64, verbose_name='Track Name')),
                ('album_name', models.CharField(max_length=64, verbose_name='Album Name')),
                ('track_length_ms', models.IntegerField(verbose_name='Track Length (ms)')),
                ('vote_count', models.IntegerField(default=0, verbose_name='Vote Count')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Added')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='crowd_control.Room')),
            ],
            options={
                'ordering': ['-vote_count', 'date_added'],
            },
        ),
        migrations.CreateModel(
            name='TrackVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_cast', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Cast')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crowd_control.Track')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='crowd_control.Room')),
                ('tracks', models.ManyToManyField(through='crowd_control.TrackVote', to='crowd_control.Track')),
            ],
        ),
        migrations.AddField(
            model_name='trackvote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crowd_control.Voter'),
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('spotify_id', 'room')]),
        ),
    ]
