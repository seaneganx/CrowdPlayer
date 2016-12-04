package com.crowdplayer;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import kaaes.spotify.webapi.android.models.Track;

public class Song implements Comparable{
    String id;
    String name;
    String artist;
    long length;
    int votes;
    long amountPlayed;

    public Song(String name, String artist, long length, int votes) {
        this.name = name;
        this.artist = artist;
        this.length = length;
        this.votes = votes;
    }

    public Song(JSONObject object) {
        try {
            id = object.getString("song_id");
            votes = object.getInt("vote_count");
            name = object.getString("song_name");
            artist = object.getString("song_artist");
        } catch (JSONException e) {
            Log.e("Song init error", e.getMessage());
        }
    }

    public Song(Track t) {
        name = t.name;
        id = t.id;
        artist = t.artists.get(0).name;
        votes = 0;
        length = t.duration_ms;
    }

    @Override
    public int compareTo(Object another) {
        return ((Song)another).votes - votes;
    }
}
