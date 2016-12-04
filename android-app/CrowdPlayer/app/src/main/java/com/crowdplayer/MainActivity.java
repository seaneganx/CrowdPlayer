package com.crowdplayer;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ExpandableListView;
import android.widget.SeekBar;
import android.widget.TextView;

import com.spotify.sdk.android.authentication.AuthenticationClient;
import com.spotify.sdk.android.authentication.AuthenticationRequest;
import com.spotify.sdk.android.authentication.AuthenticationResponse;
import com.spotify.sdk.android.player.Config;
import com.spotify.sdk.android.player.ConnectionStateCallback;
import com.spotify.sdk.android.player.Error;
import com.spotify.sdk.android.player.Player;
import com.spotify.sdk.android.player.PlayerEvent;
import com.spotify.sdk.android.player.Spotify;
import com.spotify.sdk.android.player.SpotifyPlayer;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

import kaaes.spotify.webapi.android.SpotifyApi;
import kaaes.spotify.webapi.android.SpotifyService;
import kaaes.spotify.webapi.android.models.Track;
import kaaes.spotify.webapi.android.models.TracksPager;


public class MainActivity extends AppCompatActivity implements SpotifyPlayer.NotificationCallback, ConnectionStateCallback, Player.OperationCallback {

    // TODO: Replace with your client ID
    private static final String CLIENT_ID = "26e5916c415940548e6a075ed00c6bb5";
    // TODO: Replace with your redirect URI
    private static final String REDIRECT_URI = "http://google.com";

    // Request code that will be used to verify if the result comes from correct activity
// Can be any integer
    private static final int REQUEST_CODE = 1337;

    private Player mPlayer;
    private List<Song> songs;
    private MainActivity self;
    private Song playingSong;
    private TextView songTitle;
    private TextView songArtist;
    private Handler mHandler = new Handler();
    private Handler refresh = new Handler();
    private SeekBar seekBar;
    private boolean isSeeking = false;
    private ExpandableListView playlistView;
    private PlaylistAdapter adapter;
    SpotifyApi api = new SpotifyApi();

    final SpotifyService spotify = api.getService();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        WebApiThing.deleteAll();

        self = this;
        songs = new ArrayList<>();
        songTitle = (TextView) findViewById(R.id.song_title_textView);
        songArtist = (TextView) findViewById(R.id.song_artist_textView);
        seekBar = (SeekBar) findViewById(R.id.seekBar);

        playlistView = (ExpandableListView) findViewById(R.id.playlist_listView);
        adapter = new PlaylistAdapter(this, songs);
        playlistView.setAdapter(adapter);

        AuthenticationRequest.Builder builder = new AuthenticationRequest.Builder(CLIENT_ID,
                AuthenticationResponse.Type.TOKEN,
                REDIRECT_URI);
        builder.setScopes(new String[]{"user-read-private", "streaming"});
        AuthenticationRequest request = builder.build();

        AuthenticationClient.openLoginActivity(this, REQUEST_CODE, request);

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (playingSong != null && !isSeeking && mPlayer != null && mPlayer.getPlaybackState().isPlaying) {

                    playingSong.amountPlayed += 1000;
                    seekBar.setProgress((int) playingSong.amountPlayed);
                }

                if (playingSong != null && playingSong.amountPlayed > playingSong.length - 1000) {
                    playingSong = null;


                    if (songs.size() == 0) {
                        songTitle.setText("No song selected");
                        songArtist.setText("");

                        Button b = (Button) findViewById(R.id.play_pause_button);
                        b.setText("Play");
                    } else {
                        newSong();
                    }
                }

                mHandler.postDelayed(this, 1000);
            }
        });


        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (fromUser && playingSong != null) {
                    mPlayer.seekToPosition(null, progress);
                    playingSong.amountPlayed = progress;
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                isSeeking = true;
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                isSeeking = false;
            }
        });

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                getSongs();

                refresh.postDelayed(this, 5000);
            }
        });
    }

    private void getSongs() {
        AsyncTask t = new AsyncTask() {
            @Override
            protected Object doInBackground(Object[] params) {
                JSONArray array = WebApiThing.getJson();
                Log.e("array", array.toString());

                try {
                    for (int i = 0; i < array.length(); i++) {
                        Song s = new Song(array.getJSONObject(i));
                        for (Song song : songs) {
                            if (song.id.equals(s.id)) {
                                song.votes = s.votes;
                                Log.e("Updating song", song.name);
                            }
                        }


                    }

                } catch (JSONException e) {

                }

                return null;
            }

            @Override
            protected void onPostExecute(Object object) {
                Collections.sort(songs);
                adapter = new PlaylistAdapter(self, songs);
                playlistView.setAdapter(adapter);
                adapter.notifyDataSetChanged();
            }
        };

        t.execute();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        super.onActivityResult(requestCode, resultCode, intent);

        // Check if result comes from the correct activity
        if (requestCode == REQUEST_CODE) {
            AuthenticationResponse response = AuthenticationClient.getResponse(resultCode, intent);
            if (response.getType() == AuthenticationResponse.Type.TOKEN) {
                Config playerConfig = new Config(this, response.getAccessToken(), CLIENT_ID);
                Spotify.getPlayer(playerConfig, this, new SpotifyPlayer.InitializationObserver() {
                    @Override
                    public void onInitialized(SpotifyPlayer spotifyPlayer) {
                        mPlayer = spotifyPlayer;
                        mPlayer.addConnectionStateCallback(MainActivity.this);
                        mPlayer.addNotificationCallback(MainActivity.this);
                    }

                    @Override
                    public void onError(Throwable throwable) {
                        Log.e("MainActivity", "Could not initialize player: " + throwable.getMessage());
                    }
                });
            }
        }
    }

    @Override
    protected void onDestroy() {
        // VERY IMPORTANT! This must always be called or else you will leak resources
        Spotify.destroyPlayer(this);

        mPlayer.logout();
        super.onDestroy();
    }

    @Override
    public void onPlaybackEvent(PlayerEvent playerEvent) {
        Log.d("MainActivity", "Playback event received: " + playerEvent.name());
        switch (playerEvent) {
// Handle event type as necessary
            default:
                break;
        }
    }

    @Override
    public void onPlaybackError(Error error) {
        Log.d("MainActivity", "Playback error received: " + error.name());
        switch (error) {
// Handle error type as necessary
            default:
                break;
        }
    }

    @Override
    public void onLoggedIn() {
        Log.d("MainActivity", "User logged in");

//        mPlayer.playUri(null, "spotify:track:2TpxZ7JUBn3uw46aR7qd6V", 0, 0);

    }

    @Override
    public void onLoggedOut() {
        Log.d("MainActivity", "User logged out");
    }

    @Override
    public void onLoginFailed(Error error) {
        Log.d("MainActivity", "Login failed");
    }

    @Override
    public void onTemporaryError() {
        Log.d("MainActivity", "Temporary error occurred");
    }

    @Override
    public void onConnectionMessage(String message) {
        Log.d("MainActivity", "Received connection message: " + message);
    }

    @Override
    public void onSuccess() {
        int i = 0;
    }

    @Override
    public void onError(Error error) {
        Log.d("MainActivity", "Received connection message: " + error);
    }

    public void search(View view) {
        android.widget.SearchView searchView = (android.widget.SearchView) findViewById(R.id.search_box);

        final CharSequence s = searchView.getQuery();

        if (s.equals(""))
            return;
        view.clearFocus();

        AsyncTask task = new AsyncTask<Object, Void, TracksPager>() {
            @Override
            protected TracksPager doInBackground(Object[] params) {
                TracksPager result = spotify.searchTracks(s.toString());

                return result;
            }

            @Override
            protected void onPostExecute(final TracksPager result) {
                final CharSequence[] items = new CharSequence[result.tracks.items.size()];
                int index = 0;

                for (Track t : result.tracks.items) {
                    items[index++] = t.name;
                }

                AlertDialog.Builder filterDialog = new AlertDialog.Builder(self);

                filterDialog.setSingleChoiceItems(items, -1, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                    }
                });

                filterDialog.setPositiveButton(R.string.select_song, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Track t = result.tracks.items.get(((AlertDialog) dialog).getListView().getCheckedItemPosition());
                        Song s = new Song(t);
                        songs.add(s);
                        WebApiThing.postSongSelection(s);
                    }
                });

                filterDialog.setNegativeButton(R.string.nah, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                    }
                });

                filterDialog.create().show();
            }
        };
        task.execute();
    }

    public void play(View view) {
        Button b = (Button) findViewById(R.id.play_pause_button);
        if (!mPlayer.getPlaybackState().isPlaying) {
            if (playingSong == null && songs.size() > 0) {
                newSong();
            }
            if (playingSong != null) {
                mPlayer.resume(null);
                b.setText("Pause");
            }
        } else {
            mPlayer.pause(null);
            b.setText("Play");
        }

    }

    private void newSong() {
        playingSong = songs.get(0);
        mPlayer.playUri(null, "spotify:track:" + playingSong.id, 0, 0);
        songTitle.setText(playingSong.name);
        songArtist.setText(playingSong.artist);
        seekBar.setMax((int) playingSong.length);
        songs.remove(playingSong);
        WebApiThing.deleteSong(playingSong);
    }
}



