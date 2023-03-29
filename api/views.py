from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, PlaylistSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip)
                room.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PlaylistView(APIView):
    serializer_class = PlaylistSerializer

    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            playlist_id = serializer.data.get('Playlist_id')
            playlist_name = serializer.data.get('Playlist_name')

            queryset = Playlists.objects.filter(Playlist_id=playlist_id)
            if not queryset.exists():
                Playlist = queryset[0]
                Playlist.Playlist_id = playlist_id
                Playlist.Playlist_name = playlist_name
                Playlist.save(update_fields=['Playlist_id','Playlist_name'])
            else:
                Playlist = queryset[0]
                Playlist.Playlist_id = playlist_id
                Playlist.Playlist_name = playlist_name
                Playlist.save()

            return Response(PlaylistSerializer(Playlist).data,status=status.HTTP_200_OK)

