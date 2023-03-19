from django.db import models
import uuid


class CreateUpdateDate(models.Model):
    class Meta:
        abstract = True

    # Save date and time of add and update.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class UniqueIds(models.Model):
    class Meta:
        abstract = True

    id = models.BigAutoField(primary_key=True, unique=True)
    #  public id to share with the the in url,
    #  Used for REST routes and public displays
    public_id = models.BigIntegerField(editable=False, unique=True)


class PublicId:
    # method for generating public id
    @staticmethod
    def create_public_id():
        public_id = uuid.uuid4().int >> 75
        return public_id


class BaseModel(CreateUpdateDate, UniqueIds):
    """
    Create model for inheriting purpose only.
    """

    class Meta:
        abstract = True

    pass


# Create your models here.

class Artist(BaseModel):
    """
    This model is used to store album data
    """

    class Meta:
        db_table = "artist"

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, default="evergreen", choices=[
        ("transgender", "transgender"), ("male", "male"), ("female", "female"),
    ])

    def __str__(self):
        return self.name


class Album(BaseModel):
    """
    This model is used to create table in database
    """

    class Meta:
        db_table = "album"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Track(BaseModel):
    """
    This model is used to store album data
    """

    class Meta:
        db_table = "track"

    name = models.CharField(max_length=255, )
    length = models.TimeField()
    lyrics = models.TextField()
    type = models.CharField(max_length=255, default="evergreen", choices=[
        ("evergreen", "evergreen"), ("sad", "sad"), ("sufi", "sufi"), ("romantic", "romantic"),
    ])
    album = models.ForeignKey(Album, related_name="track_album", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TrackArtist(BaseModel):
    """
    This table is used to create table in database for track artist.
    """

    class Meta:
        db_table = "track_artist"

    track = models.ForeignKey(Track, related_name="track_artist_track", on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, related_name="track_artist_female_artist", on_delete=models.CASCADE,
                               )


class PlayList(BaseModel):
    """
    This model is used to create playlist table in database
    """
    name = models.CharField(max_length=255)
    track = models.ForeignKey(Track, related_name="tp", on_delete=models.CASCADE)
