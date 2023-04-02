import requests
import base64
import json
from .models import SpotifyToken
from .credentails import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get
from django.utils import timezone
from datetime import timedelta

BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post("https://accounts.spotify.com/api/token", data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {"Content-Type": "application/json",
               'authorization': "Bearer " + tokens.access_token}

    if post:
        post(BASE_URL + endpoint, headers=headers)
    if put:
        put(BASE_URL + endpoint, headers=headers)

    Response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return Response.json()
    except:
        return {'Error': 'Issue with request'}


def create_playlist(session_key, endpoint, playlist_name, description=None, public=True, collaborative=False, post_=False, put_=False):
    # You would need to implement this function to get the access token
    tokens = get_user_tokens(session_key)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tokens.access_token
    }

    data = {
        "name": playlist_name,
        "description": description,
        "public": public,
        "collaborative": collaborative
    }
    print(data)

    response = post(BASE_URL + endpoint, headers=headers, json=data)
    print(response.json())
    if response.status_code != 201:
        return {'error': 'Failed to create playlist'}

    return response.json()
