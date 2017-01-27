from rest_framework import serializers
from crowd_control import models
from django.conf import settings

class RoomSerializer(serializers.ModelSerializer):
	host = serializers.StringRelatedField()

	class Meta:
		model = models.Room
		fields = (
			'host',
			'name',
			'creation_date',
		)

class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Track
		fields = (
			'spotify_id',
			'artist_name',
			'track_name',
			'album_name',
			'track_length_ms',
			'vote_count',
			'date_added',
		)

class QueueSerializer(serializers.ModelSerializer):
	tracks = TrackSerializer(
		read_only=True,
		many=True,
	)

	class Meta:
		model = models.Room
		fields = (
			'tracks',
		)
