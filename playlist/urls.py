from django.urls import path
from playlist.views import create_play_list, welcome, update_play_list, playlist, delete_play_list, \
    PlayListApiView, PlayListDetailApiView

urlpatterns = [
    path("welcome/", welcome, name="welcome"),
    path("create_play_list/", create_play_list, name="create_play_list"),
    path("update_play_list/<int:id>", update_play_list, name="update_play_list"),
    path("delete_play_list/<int:id>", delete_play_list, name="delete_play_list"),
    path("playlist/", playlist, name="playlist"),
    path("api/playlist/", PlayListApiView.as_view(), name="play_list_api_view"),
    path("api/playlist/<str:id>/", PlayListDetailApiView.as_view(), name="play_list_api_detail_view")
]
