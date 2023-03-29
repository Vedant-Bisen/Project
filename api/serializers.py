from rest_framework import serializers
from .models import Room, Playlists


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                  'votes_to_skip', 'created_at')


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')
        
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlists
        fields = ('Playlist_id', 'Playlist_name')
