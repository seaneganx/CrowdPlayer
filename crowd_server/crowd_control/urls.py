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
	url(r'^$', views.index, name='index'),

	url(r'^rooms/create$', views.create_room),
	url(r'^rooms/{room_param}$'.format(room_param=room_param), views.room_request),

	url(r'^queues/{room_param}$'.format(room_param=room_param), views.read_queue),
	url(r'^queues/{room_param}/{track_param}$'.format(room_param=room_param, track_param=track_param), views.queue_request
	),
]
