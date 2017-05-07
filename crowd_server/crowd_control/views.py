from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User

from crowd_control.models import Room, Track, TrackVote, Voter, Host
from crowd_control.serializers import QueueSerializer, TrackSerializer
from crowd_control.permissions import IsHost, IsHostOrReadOnly

import random, requests
from base64 import b64encode
from datetime import timedelta

class HostRegistration(APIView):

	# there are no permissions required to reach the registration views
	permission_classes = ()

	def get(self, request):

		# get the Spotify auth code from the request
		auth_code = request.GET.get('code', None)
		if auth_code is None:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		# get access and refresh tokens from Spotify before creating a user
		try:
			response = requests.post("https://accounts.spotify.com/api/token",
			headers = {
				'Authorization': "Basic " + b64encode("{client_id}:{client_secret}".format(
					client_id = settings.SPOTIFY_CLIENT_ID,
					client_secret = settings.SPOTIFY_CLIENT_SECRET,
				).encode()).decode(),
			},
			data = {
				'grant_type': "authorization_code",
				'code': auth_code,
				'redirect_uri': request.build_absolute_uri().split("?")[0], # get the request URI with the query parameters stripped off
			})
			response.raise_for_status()

		# pass back the same status code Spotify gave us if the request went bad
		except requests.HTTPError:
			return Response(status=response.status_code)

		# handle communication errors with a somewhat generic message (we don't know if it was us or Spotify)
		except (requests.ConnectionError, requests.Timeout):
			return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

		# parse the response from Spotify
		auth_response = response.json()

		# request the user's information from Spotify (we need their username at the very least)
		try:
			response = requests.get("https://api.spotify.com/v1/me",
			headers = {
				'Authorization': "Bearer {token}".format(token = auth_response['access_token']),
			})
			response.raise_for_status()

		# pass back the same status code Spotify gave us if the request went bad
		except requests.HTTPError:
			return Response(status=response.status_code)

		# handle communication errors with a somewhat generic message (we don't know if it was us or Spotify)
		except (requests.ConnectionError, requests.Timeout):
			return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

		# parse the user's data into a dictionary
		info_response = response.json()

		# create a host entry and Django user with the Spotify account information
		user, _ = User.objects.get_or_create(username = info_response['id'])
		Host.objects.update_or_create(
			spotify_id = info_response['id'],

			defaults = {
				'user': user,
				'spotify_access_token': auth_response['access_token'],
				'spotify_refresh_token': auth_response['refresh_token'],
				'spotify_access_expiry': timezone.now() + timedelta(seconds = int(auth_response['expires_in'])) - timedelta(minutes = 1),
			}
		)

		return Response({
			'access_token': user.auth_token.key,
		}, status=status.HTTP_200_OK)

class VoterRegistration(APIView):

	# there are no permissions required to reach the registration views
	permission_classes = ()

	def post(self, request, room_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# create a Django user for the voter (we need them to have an auth token)
		user = User.objects.create(
			username = "{room}_{member_count}".format(
				room=room_id,
				member_count=room.voters.count()
			)
		)

		# create a voter entry for them so they can cast votes
		Voter.objects.create(
			user = user,
			room = room,
		)

		return Response({
			'access_token': user.auth_token.key,
		}, status=status.HTTP_200_OK)

class RoomRequest(APIView):

	permission_classes = (
		IsAuthenticated,
		IsHost,
	)

	def post(self, request, room_id):

		# create a room linked to the current host and room name
		room, created = Room.objects.get_or_create(name = room_id, host = request.user.host)
		if not created:
			return Response(status=status.HTTP_409_CONFLICT)

		# create a voter profile for the host
		Voter.objects.create(
			user = request.user,
			room = room,
		)

		return Response(status=status.HTTP_201_CREATED)

	def delete(self, request, room_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)

		# tracks, voters, and votes that are related to this room all cascade upon room deletion
		room.delete()

		return Response(status=status.HTTP_200_OK)

class QueueRead(APIView):

	def get(self, request, room_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# serialize the track queue and send the response
		serializer = QueueSerializer(room)
		return Response(serializer.data, status=status.HTTP_200_OK)

class QueueUpdate(APIView):

	permission_classes = (
		IsAuthenticated,
		IsHost,
	)

	def post(self, request, room_id, track_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# attempt to retrieve the track from Spotify
		try:
			url = "https://api.spotify.com/v1/tracks/{id}".format(id=track_id)
			response = requests.get(url)
			response.raise_for_status()

		# pass back the same 4xx status code Spotify gave us if the track ID was bad
		except requests.HTTPError:
			return Response(status=response.status_code)

		# handle communication errors with a somewhat generic message (we don't know if it was us or Spotify)
		except (requests.ConnectionError, requests.Timeout):
			return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

		# parse the response from Spotify, and construct a Track object unless it already exists
		full_track = response.json()
		track, newly_created = Track.objects.get_or_create(

			# these are the only things we want to search in our get()
			room=room,
			spotify_id=track_id,

			# these will be used in addition to the others during creation of the object
			defaults={
				'artist_name': full_track['artists'][0]['name'],
				'track_name': full_track['name'],
				'album_name': full_track['album']['name'],
				'track_length_ms': full_track['duration_ms'],
			},
		)

		# serialize the track information and send the response
		serializer = TrackSerializer(track)
		return Response(
			serializer.data,
			status=status.HTTP_200_OK if newly_created else status.HTTP_409_CONFLICT,
		)

	def delete(self, request, room_id, track_id):

		# retrieve the requested track from the database
		try:
			room = Room.objects.get(pk=room_id)
			track = room.tracks.get(spotify_id=track_id)

		except (Room.DoesNotExist, Track.DoesNotExist):
			return Response(status=status.HTTP_404_NOT_FOUND)

		# votes for this track will cascade upon track deletion
		track_str = str(track)
		track.delete()

		return Response(status=status.HTTP_200_OK)

class QueueVote(APIView):

	def put(self, request, room_id, track_id, like_status):

		# determine the score for this vote
		if like_status == "like":
			like_score = 1
		else:
			like_score = 0

		# retrieve the requested track from the database
		try:
			room = Room.objects.get(pk=room_id)
			track = room.tracks.get(spotify_id=track_id)

		except (Room.DoesNotExist, Track.DoesNotExist):
			return Response(status=status.HTTP_404_NOT_FOUND)

		# create an entry for the vote in the database, otherwise update the existing entry
		vote, newly_created = TrackVote.objects.update_or_create(

			# these are the only things we want to search in our get()
			voter=request.user.voter,
			track=track,

			# these will be used in addition to the others during creation of the object
			defaults={
				'score': like_score,
			},
		)

		# serialize the track information and send the response
		serializer = TrackSerializer(track)
		return Response(serializer.data, status=status.HTTP_200_OK)
