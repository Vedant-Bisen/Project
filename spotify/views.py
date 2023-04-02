from django.shortcuts import render, redirect
from .credentails import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post, put, get
from rest_framework.response import Response
from rest_framework import status
from .models import SpotifyToken
from .util import *
from api.models import Playlists


# Create your views here.
# Scopes = user-read-playback-state user-modify-playback-state user-read-currently-playing


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = " playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative"
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
