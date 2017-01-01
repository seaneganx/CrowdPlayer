from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import random

class HostPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		return hasattr(request.user, 'host')

class RoomCreation(APIView):

	def post(self, request):

		# simple room generation for development
		adjectives = ['Gleaming', 'Junior', 'Stupendous', 'Studious', 'Cold', 'Experienced', 'Circular', 'Determined', 'Serious', 'Friendly', 'Thrifty', 'Oblong', 'Dreary', 'Decent', 'Beneficial', 'Silver', 'Splendid', 'Dreary', 'Juvenile', 'Phony', 'Black', 'Excitable', 'All', 'Threadbare', 'Farflung']
		animals = ['Lizard', 'Jackal', 'Yaffle', 'Pheasant', 'Cattle', 'Amoeba', 'Nandoo', 'JapaneseBeetle', 'Goa', 'Leafbird', 'Tahr', 'AfricanHarrierHawk', 'QueenslandHeeler', 'Gadwall', 'NeonBlueHermitCrab', 'AmericanBulldog', 'Silkworm', 'Mollusk', 'RhodesianRidgeback', 'Kangaroo', 'BlackMamba', 'IberianMidwifeToad', 'Cranefly', 'Wolf', 'Scaup']

		# generate a room name
		room_name = "{adjective1}{adjective2}{animal}".format(
			adjective1=random.choice(adjectives),
			adjective2=random.choice(adjectives),
			animal=random.choice(animals)
		)

		return Response(room_name)

class RoomRequest(APIView):

	def get(self, request, room_id):
		return Response("GET /api/rooms/{room_id}".format(room_id=room_id), status=status.HTTP_501_NOT_IMPLEMENTED)

	def delete(self, request, room_id):
		return Response("DELETE /api/rooms/{room_id}".format(room_id=room_id), status=status.HTTP_501_NOT_IMPLEMENTED)

class QueueRead(APIView):

	def get(self, request, room_id):
		return Response("GET /api/queues/{room_id}".format(room_id=room_id), status=status.HTTP_501_NOT_IMPLEMENTED)

class QueueRequest(APIView):

	def post(self, request, room_id, track_id):
		return Response("POST /api/queues/{room_id}/{track_id}".format(room_id=room_id, track_id=track_id), status=status.HTTP_501_NOT_IMPLEMENTED)

	def put(self, request, room_id, track_id):
		return Response("PUT /api/queues/{room_id}/{track_id}".format(room_id=room_id, track_id=track_id), status=status.HTTP_501_NOT_IMPLEMENTED)

	def delete(self, request, room_id, track_id):
		return Response("DELETE /api/queues/{room_id}/{track_id}".format(room_id=room_id, track_id=track_id), status=status.HTTP_501_NOT_IMPLEMENTED)
