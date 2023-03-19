from rest_framework import serializers

from playlist.models import *


class PlaylistSerializer(serializers.Serializer):
    """
    This class is used to create response for playlist
    """
    female_artist = serializers.SerializerMethodField()
    male_artist = serializers.SerializerMethodField()
    name = serializers.CharField(source="track.name")
    length = serializers.TimeField(source="track.length")
    lyrics = serializers.CharField(source="track.lyrics")
    type = serializers.CharField(source="track.type")
    album = serializers.CharField(source="track.album.name")
    id = serializers.CharField()

    class Meta:
        model = PlayList
        fields = [
            "id"
            "name",
            "length",
            "lyrics",
            "type",
            "album",
            "artist"
        ]

    def get_male_artist(self, obj):
        """
        This method is used to artist of track
        """
        return TrackArtist.objects.get(
            track=obj.track, artist__gender="male"
        ).artist.name

    def get_female_artist(self, obj):
        """
        This method is used to artist of track
        """
        return TrackArtist.objects.get(
            track=obj.track, artist__gender="female"
        ).artist.name


class AddPlaylistSerializer(serializers.Serializer):
    """
    This class is used to create response for playlist
    """

    female_artist_name = serializers.CharField(max_length=255)
    male_artist_name = serializers.CharField(max_length=255)
    track_name = serializers.CharField(max_length=255)
    length = serializers.TimeField()
    lyrics = serializers.CharField()
    type = serializers.CharField(max_length=255)
    album_name = serializers.CharField(max_length=255)

    class Meta:
        model = PlayList
        fields = [
            "female_artist",
            "male_artist",
            "track_name",
            "length",
            "lyrics",
            "type",
            "album_name",
            "artist"
        ]
