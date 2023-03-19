from unittest.mock import MagicMock, call, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response

from playlist import views
from playlist.models import PlayList
from playlist.serializers import PlaylistSerializer


class BaseTestClass(TestCase):

    # Run around classes
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # Ran between test cases
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Ran between each individual hypothesis generated example
    def setup_example(self):
        pass


class TestUserInvitationView(BaseTestClass):
    """
    This class is used to test user invitation view.
    """

    def test_create_play_list_post(self):
        """
        Test case for user invitation view.
        """
        mock_request = MagicMock(
            data={
                "female_artist_name": "Rani",
                "male_artist_name": "arijit",
                "track_name": "fdf",
                "length": "10:10",
                "lyrics": "fgjhsdf sryhae yaetgea ggggf",
                "type": "sad",
                "album_name": "dfsdfsdf"
            }
        )
        response = views.PlayListApiView.post(mock_request)
        assert 201 == response.status_code
        assert {
                   "msg": "Playlist Add successfully",
                   "status": "Success"
               } == response.data

    def test_create_play_list_get(self):
        """
        Test case for fetch user roes list view.
        """
        play_list = PlayList.objects.all()
        playlist_data = PlaylistSerializer(play_list, many=True).data
        res_data = Response(
            {"msg": "Playlist get successfully",
             "count": len(play_list),
             "status": "Success", "data": playlist_data}, status=status.HTTP_200_OK
        )

        mock_request = MagicMock({})
        results = views.PlayListApiView.get(mock_request)
        assert res_data.data == results.data
        assert 200 == results.status_code
