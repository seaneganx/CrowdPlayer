from django.db import models
from django.db.models import Min, Max

from django.utils import timezone
from django.conf import settings

from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class Host(models.Model):

	# every host is a django user
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		primary_key=True,
	)

	# every host is attached to a spotify account
	spotify_id = models.CharField(
		'Spotify user ID',
		max_length=64,
		unique=True,
	)

	spotify_access_token = models.CharField(
		'Spotify Web API Access Token',
		max_length=255,
		unique=True,
	)

	spotify_access_expiry = models.DateTimeField(
		'Spotify Access Token Expiry Date',
	)

	spotify_refresh_token = models.CharField(
		'Spotify Web API Refresh Token',
		max_length=255,
		unique=True,
	)

	def __str__(self):
		return self.spotify_id

class Room(models.Model):

	# every room is attached to a host
	host = models.OneToOneField(
		Host,
		on_delete=models.CASCADE,
	)

	# other room information
	name = models.CharField(
		'Room Name',
		max_length=32,
		primary_key=True,
	)

	creation_date = models.DateTimeField(
		'Creation Date',
		default=timezone.now,
	)

	def __str__(self):
		return self.name

class Track(models.Model):

	# every track needs to exist inside a room
	room = models.ForeignKey(
		Room,
		related_name='tracks',
		on_delete=models.CASCADE,
	)

	# other track information
	spotify_id = models.CharField(
		'Spotify track ID',
		max_length=64,
	)

	artist_name = models.CharField(
		'Artist Name',
		max_length=64,
	)
	track_name = models.CharField(
		'Track Name',
		max_length=64,
	)
	album_name = models.CharField(
		'Album Name',
		max_length=64,
	)
	track_length_ms = models.IntegerField(
		'Track Length (ms)',
	)

	date_added = models.DateTimeField(
		'Date Added',
		default=timezone.now,
	)

	class Meta:
		unique_together = ('spotify_id', 'room')

	def __str__(self):
		return "{artist} - {track}".format(
			artist=self.artist_name,
			track=self.track_name,
		)

class Voter(models.Model):

	# every voter is a django user
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		primary_key=True,
	)

	# every voter is attached to a room
	room = models.ForeignKey(
		Room,
		related_name='voters',
		on_delete=models.CASCADE,
	)

	# every voter can vote on multiple tracks
	tracks = models.ManyToManyField(
		Track,
		through='TrackVote',
		through_fields=('voter', 'track'),
	)

	def __str__(self):
		return "{short_token} ({room})".format(
			room=self.room.name,
			short_token=str(self.user.auth_token)[:6],
		)

class TrackVote(models.Model):

	# every vote must have a track being voted on
	track = models.ForeignKey(
		Track,
		on_delete=models.CASCADE,
	)

	# every vote must have a voter who cast it
	voter = models.ForeignKey(
		Voter,
		on_delete=models.CASCADE,
	)

	# every vote must have a score
	score = models.IntegerField(
		'Score',
		default=0,
	)

	# other vote info
	date_cast = models.DateTimeField(
		'Date Cast',
		default=timezone.now,
	)

	def __str__(self):
		return "{voter} | {track}".format(
			voter=self.voter,
			track=self.track,
		)
