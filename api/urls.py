from django.urls import path
from .views import RoomView, CreateRoomView, PlaylistView

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path("playlist-view", PlaylistView.as_view()),

]
