from django.shortcuts import render, redirect
from .credentails import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post, put, get
from rest_framework.response import Response
from rest_framework import status
from .models import Vote
from .util import *
from api.models import Playlists, Room


# Create your views here.
# Scopes = user-read-playback-state user-modify-playback-state user-read-currently-playing


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative"
        url = Request("GET", "https://accounts.spotify.com/authorize", params={
            "scope": scopes,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
        }).prepare().url
        return Response({"url": url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get("code")
    error = request.GET.get("error")

    response = post("https://accounts.spotify.com/api/token", data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }).json()

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    error = response.get("error")

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK)


class Playlist(APIView):
    def get(self, request, format=None):
        if not is_spotify_authenticated(self.request.session.session_key):
            request.session.create()

        endpoint = "playlists"
        response = execute_spotify_api_request(
            self.request.session.session_key, endpoint)

        if 'error' in response or 'items' not in response:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        playlist_id = []
        playlist_name = []
        playlist_owner = []
        playlist_url = []
        playlist_image = []
        items = response.get('items')
        for item in items:
            p_id = item.get('id')
            p_name = item.get('name')
            p_owner = item.get('owner').get('display_name')
            p_url = item.get('external_urls').get('spotify')
            try:
                p_image = item.get('images')[0].get('url')
            except:
                p_image = None

            playlist_id.append(p_id)
            playlist_name.append(p_name)
            playlist_owner.append(p_owner)
            playlist_url.append(p_url)
            playlist_image.append(p_image)
            # print(p_id, p_name, p_owner, p_url)

            try:
                Playlists.objects.all()

            except Playlists.DoesNotExist:
                if Playlists.objects.filter(Playlist_id=p_id).exists():
                    Playlists.objects.filter(Playlist_id=p_id).update(
                        Playlist_name=p_name, Playlist_owner=p_owner, Playlist_url=p_url)
                else:
                    Playlists.objects.create(
                        Playlist_id=p_id, Playlist_name=p_name, Playlist_owner=p_owner, Playlist_url=p_url)

        response = {
            'playlist_id': playlist_id,
            'playlist_name': playlist_name,
            'playlist_owner': playlist_owner,
            'playlist_url': playlist_url,
            'playlist_image': playlist_image,
        }

        return Response(response, status=status.HTTP_200_OK)


class CreatePlaylist(APIView):
    def post(self, request, format=None):
        if not is_spotify_authenticated(self.request.session.session_key):
            request.session.create()

        endpoint = "playlists"
        name = request.data.get('playlistName')
        description = request.data.get('description')
        public = request.data.get('public')
        collaborative = request.data.get('collaborative')
        print(name, description, public, collaborative)
        response = create_playlist(
            self.request.session.session_key, endpoint, name, description, public, collaborative)

        if 'error' in response or 'id' not in response:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        return Response(response, status=status.HTTP_201_CREATED)


class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        session_id = self.request.session.session_key
        room = Room.objects.filter(host=session_id)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)

        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""

        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name

        votes = len(Vote.objects.filter(room=room, song_id=song_id))
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': votes,
            'votes_required': room.votes_to_skip,
            'id': song_id
        }

        self.update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)

    def update_room_song(self, room, song_id):
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song'])
            votes = Vote.objects.filter(room=room).delete()


class PauseSong(APIView):
    def put(self, response, format=None):
        session_id = self.request.session.session_key
        room = Room.objects.filter(host=session_id)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response({}, status=status.HTTP_403_FORBIDDEN)


class PlaySong(APIView):
    def put(self, response, format=None):
        session_id = self.request.session.session_key
        room = Room.objects.filter(host=session_id)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response({}, status=status.HTTP_403_FORBIDDEN)


class SkipSong(APIView):
    def post(self, request, format=None):
        session_id = self.request.session.session_key
        room = Room.objects.filter(host=session_id)[0]
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.votes_to_skip

        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
            votes.delete()
            skip_song(room.host)
        else:
            vote = Vote(user=self.request.session.session_key,
                        room=room, song_id=room.current_song)
            vote.save()

        return Response({}, status.HTTP_204_NO_CONTENT)
