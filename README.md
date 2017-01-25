# CrowdPlayer

CrowdPlayer is a mobile application built for party-goers and other groups of music listeners.

It enables hosts to create a playlist based on a selection of music from Spotify (Premium users only), or their own personal music library.

Voters can connect to the room from their favourite mobile browser, then vote on songs available in the song queue, and even request for songs to be added to the song queue! The song with the highest number of votes at the time of song change will be played next.

---
### Project Overview:

##### Host Device (Android / iOS App)
- Link your Spotify Premium account to play music directly from Spotify!
- Share your personal music library in one of two modes
	- Whitelist mode: Only songs on the whitelist will be shown to voters
	- Blacklist mode: All songs except for those on the blacklist will be shown to voters
	- If a Spotify Premium account is linked, the entire Spotify catalogue is available
- Set up the room based on your administration preferences
	- Optionally require approval of new users attempting to enter the room
	- Optionally require approval of new song queue addition requests
- Select backup playlists to automatically enqueue songs if the playlist becomes too small

##### Voter Device (Mobile Web Application)
- Easily view the song queue and music library from a simple mobile website
- Cast your vote on songs to push them toward the top or bottom of the song queue
- Request new additions to the song queue from Spotify or the host's shared library
- Choose a nickname so the host knows to let you into the room
	- Don't worry, other voters can't see what you vote for

##### Server API (RESTful API)
- Acts as an interface between the host device and the voter devices
	- Any communication between the voters and the host is routed through the server by room ID
- Contains each room's song queue, which is adjusted based on legal communication from either hosts or voters
	- Voters can only request song queue additions, and vote on currently enqueued songs
	- Hosts have much more power, including song addition/removal and song order adjustment

---
### API Endpoints

##### Rooms
|  Method  |  Endpoint  |  Usage  |  Permission  |  Returns  |
| -------- | ---------- | ------- | ------------ |  -------- |
| POST | /api/rooms/create | Create a room | Host | `room_id` |
| GET | /api/rooms/`room_id` | Get a room's info | Authenticated | Room |
| DELETE | /api/rooms/`room_id` | Destroy a room | Host | - |

##### Queues
|  Method  |  Endpoint  |  Usage  |  Permission  |  Returns  |
| -------- | ---------- | ------- | ------------ |  -------- |
| GET | /api/queues/`room_id` | View queue | Authenticated | Tracks |
| POST | /api/queues/`room_id`/`track_id` | Add a track | Host | Track |
| DELETE | /api/queues/`room_id`/`track_id` | Remove a track | Host | - |
| PUT | /api/queues/`room_id`/`track_id`/like | Like a track | Authenticated | Track |
| PUT | /api/queues/`room_id`/`track_id`/unlike | Unlike a track | Authenticated | Track |


---
### Phase One (Basics):

##### 1. Web server and API
- Endpoints to control basic operations of the app
	- Vote, view room queue, etc.
- Authentication design for voters and hosts
	- How can we prevent malicious voters from taking control of the song queue?
	- How do we verify requests from hosts or voters?

##### 2.1 Android app
- Basic features only (connect account, manage playlist, vote, etc.)
- App redesign will happen when the iOS app is made

##### 2.2 Custom flow for Spotify OAuth
- Spotify Android/iOS SDK doesn't receive refresh tokens during the standard OAuth flow
	- Solution found here: https://github.com/spotify/android-sdk/issues/10
- I have to send the authorizaton code to the server where I can request an access token together with a refresh token
- The access token, refresh token, and access token expiry date will be stored in the server database
- The alternative is having a 3600 second (one hour) expiry on the authorizaton, which requires the host to log into Spotify again (lame) on their phone to refresh the token

##### 3. Voter website (mobile web app)
- Make a pretty mobile interface with song listing and a vote button
- Display current song information
- Potentially make a song progress slider

### Phase Two (Bonus features)

##### 1. Song requests
- Endpoints for voters to request songs in a given room, and for hosts to see requests
- App must be able to search the entire Spotify library in a reasonable way on the front-end
- Hosts must be able to reject or approve song requests
- Allow users to search for songs in the Spotify library
	- Search by artist, album, track

##### 2. Android / iOS App Redesign
- Create a prettier looking app with more functionality
- At this point the app can be released into the wild

##### 2. Host user registration
- Securely verify whether a potential host is a robot (highly unlikely with Google Play / Spotify accounts)
- Remove required link to Spotify Premium account

##### 3. Personal library support
- Specific communication with the server regarding the type of song being listed (Spotify vs. Local)
- Ability to play music files off the host's device rather than Spotify player

##### 4. Customized shared library
- Host can whitelist / blacklist songs, artists, and albums
- Voters will only be able to request songs from the available library

---
### Decisions:
- How should the front-end be written?
	- Django templates?
- Which hosting platform should I use?
- At what stage should I deploy the app to the public?
- To advertise, or not to advertise, that is the question: Whether 'tis Nobler in the mind to suffer...
- How many measures should be put in place to prevent vote spoofing?
	- Nicknames with host approval? Voter registration (great way to have nobody use the app)
	- This is the question I'm having the most trouble answering
