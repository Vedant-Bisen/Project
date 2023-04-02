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
        items = response.get('items')
        for item in items:
            playlist_id.append(item.get('id'))
            playlist_name.append(item.get('name'))
            playlist_owner.append(item.get('owner').get('display_name'))
            playlist_url.append(item.get('external_urls').get('spotify'))

        for i in range(len(playlist_id)):
            Playlists.objects.create(
                Playlist_id=playlist_id[i], Playlist_name=playlist_name[i], Playlist_owner=playlist_owner[i], Playlist_url=playlist_url[i])

        response = {
            'playlist_id': playlist_id,
            'playlist_name': playlist_name,
            'playlist_owner': playlist_owner,
            'playlist_url': playlist_url,
        }

        return Response(response, status=status.HTTP_200_OK)
