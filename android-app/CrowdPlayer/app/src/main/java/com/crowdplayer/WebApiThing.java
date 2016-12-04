package com.crowdplayer;

import android.net.Uri;
import android.os.AsyncTask;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URL;

public class WebApiThing {
    public static JSONArray getJson() {
        try{
            URL url = new URL("http://frozenbomb.com/app/get.php");
            java.util.Scanner s = new java.util.Scanner(url.openStream()).useDelimiter("\\A");
            String myString = s.hasNext() ? s.next() : "";
            JSONArray arr = new JSONObject(myString).getJSONArray("array");
            arr.toString();
            return arr;
        }catch(Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }

    public static void postSongSelection(Song song) {
        final String url = Uri.parse(String.format("http://frozenbomb.com/app/new.php/?id=%s&name=%s&artist=%s", song.id, song.name, song.artist)).buildUpon().build().toString();
        doThings(url);
    }

    public static void deleteSong(Song song) {
        final String url = Uri.parse(String.format("http://frozenbomb.com/app/delete.php/?id=%s", song.id)).buildUpon().build().toString();
        doThings(url);
    }

    public static void deleteAll() {
        final String url = Uri.parse("http://frozenbomb.com/app/deleteall.php").buildUpon().build().toString();
        doThings(url);
    }

    private static void doThings(String originalUrl) {
        final String url = originalUrl.replaceAll(" ", "%20");
        AsyncTask t = new AsyncTask() {
            @Override
            protected Object doInBackground(Object[] params) {
                try {
                    new URL(url).openStream().close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return null;
            }
        };

        t.execute();
    }

}


