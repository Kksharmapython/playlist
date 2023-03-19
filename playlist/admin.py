from django.contrib import admin
from playlist.models import Album, Artist, PlayList, TrackArtist, Track


# Register your models here.
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "gender",
    ]


@admin.register(TrackArtist)
class TrackArtistAdmin(admin.ModelAdmin):
    list_display = [
        "track",
        "artist",
    ]


@admin.register(Track)
class TrackArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "length",
        "lyrics",
        "type",
        "album",
    ]


admin.site.register(Album)
