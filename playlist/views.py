from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from playlist.models import *
from playlist.serializers import PlaylistSerializer, AddPlaylistSerializer


# Create your views here.
def welcome(request):
    """
    This fun is used to open landing page.
    """
    return render(request, "welcome.html")


def create_play_list(request):
    if request.method == "POST":
        try:
            album = Album.objects.get(
                name=request.POST["album_name"]
            )
        except Album.DoesNotExist:

            album = Album.objects.create(
                public_id=PublicId.create_public_id(),
                name=request.POST["album_name"]
            )

        track = Track.objects.create(
            public_id=PublicId.create_public_id(),
            name=request.POST["track_name"],
            length=request.POST["length"],
            lyrics=request.POST["lyrics"],
            type=request.POST["type"],
            album=album
        )
        if request.POST.get("male_artist_name"):
            try:
                artist = Artist.objects.get(
                    name=request.POST.get("male_artist_name"), gender="male"
                )
            except Artist.DoesNotExist:

                artist = Artist.objects.create(
                    public_id=PublicId.create_public_id(),
                    gender="male",
                    name=request.POST.get("male_artist_name")
                )
            TrackArtist.objects.create(
                public_id=PublicId.create_public_id(),
                track=track,
                artist=artist,

            )
        if request.POST.get("female_artist_name"):
            try:
                artist = Artist.objects.get(
                    name=request.POST.get("female_artist_name"), gender="    female"
                )
            except Artist.DoesNotExist:

                artist = Artist.objects.create(
                    public_id=PublicId.create_public_id(),
                    gender="female",
                    name=request.POST.get("female_artist_name")
                )
            TrackArtist.objects.create(
                public_id=PublicId.create_public_id(),
                track=track,
                artist=artist,

            )
        playlist = PlayList.objects.create(
            public_id=PublicId.create_public_id(),
            track=track,
            name=request.POST["album_name"],

        )

    return render(request, "create_play_list.html")


def update_play_list(request, id):
    play_list = PlayList.objects.get(id=id)
    if request.method == "POST":
        if request.POST.get("album_name"):
            play_list.track.album.name = request.POST["album_name"]
            play_list.track.album.save()

        Track.objects.filter(
            public_id=play_list.track.public_id).update(
            name=request.POST["track_name"],
            length=request.POST["length"],
            lyrics=request.POST["lyrics"],
            type=request.POST["type"],
        )
        if request.POST.get("male_artist_name"):
            track_artist = TrackArtist.objects.get(track=play_list.track, artist__gender="male")
            track_artist.artist.name = request.POST.get("male_artist_name")
            track_artist.artist.save()

        if request.POST.get("female_artist_name"):
            track_artist = TrackArtist.objects.get(track=play_list.track, artist__gender="female")
            track_artist.artist.name = request.POST.get("female_artist_name")
            track_artist.artist.save()
        playlist = PlaylistSerializer(PlayList.objects.all(), many=True).data
        return render(request, "playlist_list.html", {"datas": playlist})

    playlist = PlaylistSerializer(play_list).data
    return render(request, "update_playlist.html", {"data": playlist})


def playlist(request):
    playlist = PlaylistSerializer(PlayList.objects.all(), many=True).data
    return render(request, "playlist_list.html", {"datas": playlist})


def delete_play_list(request, id):
    play_list = PlayList.objects.get(id=id)
    play_list.track.album.delete()
    Track.objects.filter(
        public_id=play_list.track.public_id).delete()
    play_list.delete()
    playlist = PlaylistSerializer(PlayList.objects.all(), many=True).data
    return render(request, "playlist_list.html", {"datas": playlist})


class PlayListApiView(APIView):
    """

    """

    @classmethod
    def post(cls, request):
        serial = AddPlaylistSerializer(data=request.data)
        if serial.is_valid(raise_exception=True):
            serial_data = serial.validated_data
            try:
                album = Album.objects.get(
                    name=serial_data["album_name"]
                )
            except Album.DoesNotExist:

                album = Album.objects.create(
                    public_id=PublicId.create_public_id(),
                    name=serial_data["album_name"]
                )

            track = Track.objects.create(
                public_id=PublicId.create_public_id(),
                name=serial_data["track_name"],
                length=serial_data["length"],
                lyrics=serial_data["lyrics"],
                type=serial_data["type"],
                album=album
            )
            if serial_data.get("male_artist_name"):
                try:
                    artist = Artist.objects.get(
                        name=serial_data.get("male_artist_name"), gender="male"
                    )
                except Artist.DoesNotExist:

                    artist = Artist.objects.create(
                        public_id=PublicId.create_public_id(),
                        gender="male",
                        name=serial_data.get("male_artist_name")
                    )
                TrackArtist.objects.create(
                    public_id=PublicId.create_public_id(),
                    track=track,
                    artist=artist,

                )
            if serial_data.get("female_artist_name"):
                try:
                    artist = Artist.objects.get(
                        name=serial_data.get("female_artist_name"), gender="    female"
                    )
                except Artist.DoesNotExist:

                    artist = Artist.objects.create(
                        public_id=PublicId.create_public_id(),
                        gender="female",
                        name=serial_data.get("female_artist_name")
                    )
                TrackArtist.objects.create(
                    public_id=PublicId.create_public_id(),
                    track=track,
                    artist=artist,

                )
            playlist = PlayList.objects.create(
                public_id=PublicId.create_public_id(),
                track=track,
                name=serial_data["album_name"],

            )
            # playlist = PlaylistSerializer(playlist).data
            return Response(
                {"msg": "Playlist Add successfully",
                 "status": "Success", }, status=status.HTTP_201_CREATED
            )

    @classmethod
    def get(cls, request):
        play_list = PlayList.objects.all()
        playlist_data = PlaylistSerializer(play_list, many=True).data

        return Response(
            {"msg": "Playlist get successfully",
             "count": len(play_list),
             "status": "Success", "data": playlist_data}, status=status.HTTP_200_OK
        )


class PlayListDetailApiView(APIView):
    """

    """

    @classmethod
    def get(cls, request, id):
        play_list = PlayList.objects.get(id=id)
        playlist_data = PlaylistSerializer(play_list, ).data

        return Response(
            {"msg": "Playlist get successfully",
             "status": "Success", "data": playlist_data}, status=status.HTTP_200_OK
        )

    @classmethod
    def delete(cls, request, id):
        play_list = PlayList.objects.filter(id=id).delete()
        return Response(
            {"msg": "Playlist delete successfully",
             "status": "Success"}, status=status.HTTP_200_OK
        )

    @classmethod
    def patch(cls, request, id):
        play_list = PlayList.objects.get(id=id)

        if request.POST.get("album_name"):
            play_list.track.album.name = request.POST["album_name"]
            play_list.track.album.save()

        Track.objects.filter(
            public_id=play_list.track.public_id).update(
            name=request.POST["track_name"],
            length=request.POST["length"],
            lyrics=request.POST["lyrics"],
            type=request.POST["type"],
        )
        if request.POST.get("male_artist_name"):
            track_artist = TrackArtist.objects.get(track=play_list.track, artist__gender="male")
            track_artist.artist.name = request.POST.get("male_artist_name")
            track_artist.artist.save()

        if request.POST.get("female_artist_name"):
            track_artist = TrackArtist.objects.get(track=play_list.track, artist__gender="female")
            track_artist.artist.name = request.POST.get("female_artist_name")
            track_artist.artist.save()
        return Response(
            {"msg": "Playlist update successfully",
             "status": "Success"}, status=status.HTTP_200_OK
        )