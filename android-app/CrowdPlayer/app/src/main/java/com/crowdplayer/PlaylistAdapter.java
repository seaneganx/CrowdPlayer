package com.crowdplayer;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseExpandableListAdapter;
import android.widget.TextView;

import java.util.Collections;
import java.util.List;

public class PlaylistAdapter extends BaseExpandableListAdapter {
    private Context context;
    private List<Song> songs;
    private LayoutInflater inflater;

    public PlaylistAdapter(Context context, List<Song> songs) {
        this.context = context;
        this.songs = songs;
        inflater = ((Activity) context).getLayoutInflater();
    }

    @Override
    public int getGroupCount() {
        return songs.size();
    }

    @Override
    public int getChildrenCount(int groupPosition) {
        return 1;
    }

    @Override
    public Object getGroup(int groupPosition) {
        return songs.get(groupPosition);
    }

    @Override
    public Object getChild(int groupPosition, int childPosition) {
        return songs.get(groupPosition).name;
    }

    @Override
    public long getGroupId(int groupPosition) {
        return groupPosition;
    }

    @Override
    public long getChildId(int groupPosition, int childPosition) {
        return childPosition;
    }

    @Override
    public boolean hasStableIds() {
        return false;
    }

    @Override
    public boolean isChildSelectable(int groupPosition, int childPosition) {
        return true;
    }

    @Override
    public View getGroupView(int groupPosition, boolean isExpanded, View convertView, ViewGroup parent) {
        View row = convertView;
        SongHolder holder;

        if (row == null) {
            row = inflater.inflate(R.layout.playlist_row, parent, false);

            holder = new SongHolder();
            holder.name = (TextView) row.findViewById(R.id.row_song_name);
            holder.votes = (TextView) row.findViewById(R.id.row_song_votes);
            holder.artist = (TextView) row.findViewById(R.id.row_artist_name);

            row.setTag(holder);
        } else {
            holder = (SongHolder) row.getTag();
        }

        Song song = songs.get(groupPosition);

        holder.name.setText(song.name);
        holder.artist.setText(song.artist);
        holder.votes.setText("\tVotes: " + Integer.toString(song.votes));

        return row;
    }

    @Override
    public View getChildView(int groupPosition, int childPosition, boolean b, View view, ViewGroup viewGroup) {
        TextView textView = new TextView(context);
        String s = ((Song) getGroup(groupPosition)).name;
        textView.setText(s);
        return textView;
    }

    private static class SongHolder {
        TextView name;
        TextView votes;
        TextView artist;
    }
}