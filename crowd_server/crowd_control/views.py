from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError

from crowd_control.models import Room, Track, TrackVote, Voter
from crowd_control.serializers import RoomSerializer, QueueSerializer, TrackSerializer
from crowd_control.permissions import IsHost, IsHostOrReadOnly
from rest_framework.permissions import IsAuthenticated

import random, requests

class HostRegistration(APIView):

	# there are no permissions required to reach the registration views
	permission_classes = ()

	def post(self, request):
		return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

class VoterRegistration(APIView):

	# there are no permissions required to reach the registration views
	permission_classes = ()

	def post(self, request):
		return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

class RoomCreation(APIView):

	permission_classes = (
		IsAuthenticated,
		IsHost,
	)

	def post(self, request):

		# find the host information for this user
		host = request.user.host

		# simple room generation for development
		adjectives = ['Able','Back','Bad','Baggy','Bare','Basic','Calm','Damp','Dark','Dead','Dear','Each','Eager','Early','Easy','Faint','Fair','Fake','Fancy','Far','Giant','Giddy','Hairy','Half','Handy','Happy','Hard','Icky','Icy','Ideal','Idle','Ill','Jaded','Keen','Lame','Lanky','Large','Last','Late','Mad','Major','Male','Naive','Nasty','Obese','Oily','Pale','Past','Rapid','Rare','Rash','Raw','Sad','Safe','Salty','Same','Sandy','Sane','Scaly','Scary','Tall','Tame','Tan','Tart','Tasty','Taut','Ugly','Vague','Vain','Valid','Wan','Warm','Wary','Wavy','Zany','False','Adept','Aged','Best','Big','Black','Cheap','Chief','Clean','Clear','Close','Deep','Fast','Fat','Fatal','Few','Glass','Harsh','Hasty','Key','Kind','Lazy','Leafy','Lean','Left','Legal','Light','Mealy','Mean','Meaty','Near','Neat','Needy','Odd','Old','Perky','Pesky','Petty','Phony','Pink','Plain','Ready','Real','Red','Regal','Shady','Sharp','Shiny','Short','Showy','Shy','Sick','Silky','Tense','Tepid','Testy','That','These','Unfit','Vapid','Vast','Weak','Weary','Wee','Weepy','Weird','Agile','Ajar','Alert','Alive','All','Bland','Blank','Bleak','Blind','Blond','Blue','Cold','Dense','Empty','Fine','Firm','First','Fixed','Flaky','Flat','Glum','Good','Heavy','Hefty','Joint','Jolly','Limp','Lined','Meek','Merry','Messy','Mild','New','Only','Open','Plump','Plush','Silly','Slim','Slimy','Slow','Small','Smart','Smug','Thick','Thin','Third','This','Those','Wet','Which','Zesty','Ample','Angry','Bogus','Bold','Bony','Bossy','Both','Bowed','Cool','Dim','Equal','Fluid','Fond','Grand','Grave','Gray','Great','Green','High','Live','Livid','Lone','Long','Milky','Minor','Minty','Misty','Mixed','Next','Nice','Nifty','Nippy','Poor','Posh','Quick','Rich','Right','Rigid','Ripe','Soft','Soggy','Solid','Some','Sore','Soupy','Sour','Spicy','Spry','Tidy','Tight','Tiny','Tired','Torn','Total','White','Whole','Wide','Wild','Windy','Young','Any','Apt','Arid','Brave','Brief','Brisk','Brown','Corny','Crazy','Crisp','Dirty','Dizzy','Dopey','Even','Every','Evil','Frail','Frank','Free','Fresh','Grim','Grimy','Gross','Hot','Huge','Juicy','Jumbo','Loose','Lost','Loud','Moist','Moral','Noisy','Noted','Other','Our','Prime','Prize','Quiet','Rosy','Rough','Round','Rowdy','Staid','Stale','Stark','Steel','Steep','Stiff','Tough','Trim','Wiry','Wise','Witty','Woozy','Wordy','Worn','Aware','Awful','Bulky','Bumpy','Burly','Busy','Cruel','Curly','Curvy','Cute','Drab','Dry','Dual','Dull','Front','Full','Funny','Fussy','Fuzzy','Grown','Gummy','Husky','Itchy','Jumpy','Known','Kooky','Low','Loyal','Lucky','Lumpy','Muddy','Murky','Mushy','Musty','Muted','Novel','Numb','Nutty','Oval','Proud','Puny','Pure','Pushy','Royal','Ruddy','Rude','Runny','Rural','Rusty','Sunny','Super','Sweet','Swift','Tubby','Twin','Upset','Urban','Used','Utter','Vital','Vivid','Worse','Worst','Wrong','Wry','Yummy','True','Aqua','Azure','Beige','Black','Blue','Brown','Coral','Cyan','Gold','Gray','Green','Ivory','Khaki','Lime','Linen','Navy','Olive','Peru','Pink','Plum','Red','Snow','Tan','Teal','Wheat','White']
		animals = ['Addax','Adder','Agama','Aidi','Anole','Ant','Anura','Ape','Aphid','Asp','Ass','Auk','Baiji','Barb','Basil','Bass','Bat','Bats','Bear','Bee','Bilby','Bird','Bison','Bluet','Boa','Boar','Bongo','Booby','Borer','Boto','Boutu','Brant','Bream','Buck','Bufeo','Bug','Bull','Bunny','Burro','Calf','Camel','Carp','Cat','Cats','Cavy','Cero','Chick','Civet','Clam','Coati','Cob','Cobra','Cock','Cod','Colt','Comet','Conch','Coney','Cony','Coot','Coqui','Coral','Cow','Coypu','Crab','Crane','Crow','Cub','Cur','Deer','Degu','Degus','Dingo','Dodo','Doe','Dog','Dore','Dove','Drake','Duck','Eagle','Eel','Eeve','Eft','Egg','Egret','Eider','Eland','Elk','Elver','Emu','Erin','Erne','Esok','Ewe','Eyas','Eyra','Fawn','Finch','Fish','Flea','Flee','Flies','Fluke','Fly','Foal','Fossa','Fowl','Fox','Frog','Fugu','Galah','Gar','Gaur','Gecko','Geese','Genet','Gnat','Gnu','Goa','Goat','Goose','Goral','Grebe','Grub','Gull','Guppy','Hake','Hare','Hart','Hawk','Hen','Heron','Hind','Hog','Hoiho','Hoki','Horse','Hound','Huia','Human','Husky','Hydra','Hyena','Hyrax','Ibex','Ibis','Imago','Indri','Jay','Jenny','Joey','Junco','Kagu','Kid','Kite','Kitty','Kiwi','Koala','Kob','Koi','Krill','Kudu','Lamb','Lark','Larva','Lcont','Leech','Lemur','Lice','Liger','Ling','Lion','Llama','Lobo','Loon','Loris','Louse','Lynx','Macaw','Mamba','Manta','Mara','Mare','Mice','Midge','Mink','Mite','Moa','Mole','Molly','Moose','Moray','Moth','Mouse','Mule','Mutt','Myna','Mynah','Nag','Naga','Nandu','Nene','Nerka','Newt','Noddy','Nyala','Nymph','Okapi','Olm','Orca','Oryx','Otter','Owl','Ox','Oxen','Panda','Perch','Pewee','Pig','Pika','Pike','Pipit','Polyp','Pony','Pooch','Prawn','Pug','Puma','Pupa','Puppy','Pygmy','Quail','Quoll','Racer','Rail','Ram','Rat','Raven','Ray','Rhea','Rhino','Roach','Roan','Robin','Rook','Sable','Saiga','Scaup','Seal','Shark','Sheep','Shrew','Skink','Skua','Skunk','Sloth','Slug','Smew','Snail','Snake','Snipe','Sora','Sow','Squab','Squid','Stag','Steed','Steer','Stilt','Stoat','Stork','Stud','Swan','Swift','Tahr','Takin','Tapir','Tayra','Teal','Tegus','Tench','Tern','Thrip','Tick','Tiger','Titi','Toad','Topi','Trex','Trout','Tuna','Unau','Upupa','Urial','Urson','Urubu','Urus','Urutu','Urva','Veery','Viper','Vireo','Vixen','Vole','Wasp','Whale','Whelp','Wolf','Worm','Wren','Xeme','Xerus','Xoni','Yak','Yapok','Yeti','Zebra','Zebu','Zeren']

		# generate a room name
		room_name = "{adjective}{animal}".format(
			adjective=random.choice(adjectives),
			animal=random.choice(animals),
		)

		# create a room linked to the current host and room name
		room = Room(
			name=room_name,
			host=host,
		)

		# create a voter profile for the host
		voter = Voter(
			user=request.user,
			room=room,
		)

		# attempt to save the room and voter, handling any exceptions that occur
		try:
			room.save()
			voter.save()
		except IntegrityError as e:
			return Response("{user} is already hosting a room.".format(user=host), status=status.HTTP_400_BAD_REQUEST)

		# serialize and return the room data
		serializer = RoomSerializer(room)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class RoomRequest(APIView):

	permission_classes = (
		IsAuthenticated,
		IsHostOrReadOnly,
	)

	def get(self, request, room_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)

		# serialize the room information and send the response
		serializer = RoomSerializer(room)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def delete(self, request, room_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)

		# tracks, voters, and votes that are related to this room all cascade upon room deletion
		room.delete()

		return Response("The room {room} and its related data were successfully deleted.".format(room=room_id), status=status.HTTP_200_OK)

class QueueRead(APIView):

	def get(self, request, room_id):

		# retrieve the requested room from the database
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)

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
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)

		# attempt to retrieve the track from Spotify
		try:
			url = "https://api.spotify.com/v1/tracks/{id}".format(id=track_id)
			response = requests.get(url)
			response.raise_for_status()

		# pass back the same 4xx status code Spotify gave us if the track ID was bad
		except requests.HTTPError:
			return Response("The track ID {id} was rejected by Spotify".format(id=track_id), status=response.status_code)

		# handle communication errors with a somewhat generic message (we don't know if it was us or Spotify)
		except (requests.ConnectionError, requests.Timeout):
			return Response("We had some trouble communicating with Spotify", status=status.HTTP_503_SERVICE_UNAVAILABLE)

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
		except Room.DoesNotExist:
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)
		except Track.DoesNotExist:
			return Response("The track {id} could not be found in {room}.".format(id=track_id, room=room_id), status=status.HTTP_404_NOT_FOUND)

		# votes for this track will cascade upon track deletion
		track_str = str(track)
		track.delete()

		return Response("The track {name} and its votes were successfully deleted.".format(name=track_str), status=status.HTTP_200_OK)

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
		except Room.DoesNotExist:
			return Response("The room {room} could not be found.".format(room=room_id), status=status.HTTP_404_NOT_FOUND)
		except Track.DoesNotExist:
			return Response("The track {id} could not be found in {room}.".format(id=track_id, room=room_id), status=status.HTTP_404_NOT_FOUND)

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
