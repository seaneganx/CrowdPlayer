# CrowdPlayer

CrowdPlayer is a mobile application built for party-goers and other groups of music listeners.

It enables hosts to create a playlist based on a selection of music from Spotify (Premium users only), or their own personal music library.

Voters can connect to the room from their favourite mobile browser, then vote on songs available in the song queue, and even request for songs to be added to the song queue! The song with the highest number of votes at the time of song change will be played next.

---
### Feature List:

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
