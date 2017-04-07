from django.conf.urls import url

from crowd_control import views

# define the names of each URL parameter, and limit the format using regex
room_param = "(?P<{param_name}>{room_regex})".format(
	param_name="room_id",
	room_regex="[a-zA-Z]+"
)
track_param = "(?P<{param_name}>{track_regex})".format(
	param_name="track_id",
	track_regex="[a-zA-Z0-9]+"
)
like_param = "(?P<{param_name}>{like_regex})".format(
	param_name="like_status",
	like_regex="like|unlike"
)

urlpatterns = [
	url(r'^register$', views.HostRegistration.as_view()),

	url(r'^rooms/create$', views.RoomCreation.as_view()),
	url(r'^rooms/{room_param}$'.format(room_param=room_param), views.RoomRequest.as_view()),
	url(r'^rooms/{room_param}/register$'.format(room_param=room_param), views.VoterRegistration.as_view()),

	url(r'^queues/{room_param}$'.format(room_param=room_param), views.QueueRead.as_view()),
	url(r'^queues/{room_param}/{track_param}$'.format(room_param=room_param, track_param=track_param), views.QueueUpdate.as_view()),
	url(r'^queues/{room_param}/{track_param}/{like_param}$'.format(room_param=room_param, track_param=track_param, like_param=like_param), views.QueueVote.as_view()),
]
