from django.conf.urls import url

from . import views

# define the names of each URL parameter, and limit the format using regex
room_param = "(?P<{param_name}>{room_regex})".format(
	param_name="room_id",
	room_regex="[a-zA-Z]+"
)
track_param = "(?P<{param_name}>{track_regex})".format(
	param_name="track_id",
	track_regex="[a-zA-Z0-9]+"
)

urlpatterns = [
	url(r'^rooms/create$', views.RoomCreation.as_view()),
	url(r'^rooms/{room_param}$'.format(room_param=room_param), views.RoomRequest.as_view()),

	url(r'^queues/{room_param}$'.format(room_param=room_param), views.QueueRead.as_view()),
	url(r'^queues/{room_param}/{track_param}$'.format(room_param=room_param, track_param=track_param), views.QueueRequest.as_view()),
]
