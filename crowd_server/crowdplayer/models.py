from django.db import models

# Create your models here.
class Host(models.Model):

	# every host is attached to a spotify account
	spotify_id = models.CharField(max_length=50)

	# host info
	name = models.CharField(max_length=50)
	reg_date = models.DateTimeField()

	def __str__(self):
		return "{name}: {spotify}".format(name=name, spotify=spotify_id)

class Room(models.Model):

	# room info
	name = models.CharField(max_length=50)

	# every room needs a host
	host = models.ForeignKey(Host, on_delete=models.CASCADE)

	def __str__(self):
		return "{name} ({host})".format(name=name, host=host)

class Song(models.Model):

	# what is the spotify ID of the song?
	spotify_id = models.CharField(max_length=50)

	# song info
	name = models.CharField(max_length=50)
	artist = models.CharField(max_length=50)
	votes = models.IntegerField(default=0)
	length = models.IntegerField() # number of seconds

	# every song needs to exist inside a room
	room = models.ForeignKey(Room, on_delete=models.CASCADE)

	def __str__(self):
		return "Votes: {count}, {artist} - {name}".format(count=votes, room=room, artist=artist, name=name)
