from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from crowd_control.models import Host, Room, Track

# Create your views here.
def index(request):
	return HttpResponse("CrowdPlayer is currently in development.")

@api_view(['POST'])
def create_room(request):

	if request.method == 'POST':
		return Response("POST /api/rooms/create/", status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET', 'DELETE'])
def room_request(request, room_id):

	if request.method == 'GET':
		return Response("GET /api/rooms/{room_id})".format(room_id=room_id), status=status.HTTP_501_NOT_IMPLEMENTED)

	elif request.method == 'DELETE':
		return Response("DELETE /api/rooms/{room_id})".format(room_id=room_id), status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
def read_queue(request, room_id):

	if request.method == 'GET':
		return Response("GET /api/queues/{room_id})".format(room_id=room_id), status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['POST', 'PUT', 'DELETE'])
def queue_request(request, room_id, track_id):

	if request.method == 'POST':
		return Response("POST /api/queues/{room_id}/{track_id})".format(room_id=room_id, track_id=track_id), status=status.HTTP_501_NOT_IMPLEMENTED)

	elif request.method == 'PUT':
		return Response("PUT /api/queues/{room_id}/{track_id})".format(room_id=room_id, track_id=track_id), status=status.HTTP_501_NOT_IMPLEMENTED)

	elif request.method == 'DELETE':
		return Response("DELETE /api/queues/{room_id}/{track_id})".format(room_id=room_id, track_id=track_id), status=status.HTTP_501_NOT_IMPLEMENTED)
