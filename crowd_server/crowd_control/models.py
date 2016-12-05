from django.db import models
from django.db.models import Min, Max

from django.utils import timezone

# Create your models here.
class Host(models.Model):

	# every host is attached to a spotify account
	spotify_id = models.CharField(
		'Spotify user ID',
		max_length=64
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
	creation_date = models.DateTimeField(
		'Creation Date',
		default=timezone.now
	)

	def get_track_queue(self):

		# sort the tracks by vote count, with oldest track ID at the top
		return self.track_set.order_by('-vote_count', 'id')

	def __str__(self):
		return "{host}'s Room".format(
			host=self.host.spotify_id
		)

class Track(models.Model):

	# every track needs to exist inside a room
	room = models.ForeignKey(
		Room,
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

	def __str__(self):
		return "{artist} - {track} ({votes})".format(
			artist=self.artist_name,
			track=self.track_name,
			votes=self.vote_count
		)
