from django.db import models
from django.db.models import Min, Max

from django.utils import timezone

from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
# Create your models here.
class Host(models.Model):

	# every host is attached to a spotify account
	spotify_id = models.CharField(
		'Spotify user ID',
		max_length=64,
		primary_key=True
	)

	# spotify auth token information shouldn't be shown on forms
	spotify_access_token = models.CharField(
		'Spotify Web API Access Token',
		max_length=128
	)

	spotify_access_expiry = models.DateTimeField(
		'Spotify Access Token Expiry Date',
		default=timezone.now
	)

	spotify_refresh_token = models.CharField(
		'Spotify Web API Refresh Token',
		max_length=128
	)

	# other host information
	reg_date = models.DateTimeField(
		'Registration Date',
		default=timezone.now
	)

	def __str__(self):
		return self.spotify_id

class Room(models.Model):

	# every room is attached to a host
	host = models.OneToOneField(
		Host,
		on_delete=models.CASCADE
	)

	# other room information
	room_name = models.CharField(
		'Room Name',
		max_length=32,
		primary_key=True
	)

	creation_date = models.DateTimeField(
		'Creation Date',
		default=timezone.now
	)

	def get_next_track(self):

		# there is no next track if there are no tracks in the room
		tracks = self.tracks
		if tracks.count() == 0:
			return None

		# find the tracks with the most votes
		max_votes = tracks.aggregate(Max('vote_count'))['vote_count__max']
		top_tracks = tracks.filter(vote_count=max_votes)

		# find the oldest track in the top_tracks queryset
		min_id = top_tracks.aggregate(Min('id'))['id__min']
		next_track = top_tracks.get(id = min_id)

		return next_track

	def get_track_queue(self):

		# sort the tracks by vote count, with oldest track ID at the top
		return self.tracks.order_by('-vote_count', 'id')

	def __str__(self):
		return "{host}'s Room ({id})".format(
			host=self.host.spotify_id,
			id=self.room_name
		)

class Track(models.Model):

	# every track needs to exist inside a room
	room = models.ForeignKey(
		Room,
		related_name='tracks',
		on_delete=models.CASCADE
	)

	# other track information
	spotify_id = models.CharField(
		'Spotify track ID',
		max_length=64
	)

	artist_name = models.CharField(
		'Artist Name',
		max_length=64
	)
	track_name = models.CharField(
		'Track Name',
		max_length=64
	)
	album_name = models.CharField(
		'Album Name',
		max_length=64
	)
	track_length_ms = models.IntegerField(
		'Track Length (ms)'
	)

	vote_count = models.IntegerField(
		'Vote Count',
		default=0
	)

	date_added = models.DateTimeField(
		'Date Added',
		default=timezone.now
	)

	class Meta:
		unique_together = ('spotify_id', 'room')
		ordering = ['-vote_count', 'date_added']

	def __str__(self):
		return "{artist} - {track} ({votes})".format(
			artist=self.artist_name,
			track=self.track_name,
			votes=self.vote_count
		)
