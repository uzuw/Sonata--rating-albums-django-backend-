from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
import re
from external_data.services import fetch_all_albums,fetch_album_by_id, fetch_tracks_for_album, find_album_by_name
from .models import Rating
from .serializers import RatingSerializer

class AlbumViewSet(viewsets.ViewSet):
    """
    Simplified ViewSet for fetching albums and their tracks from Spotify API.
    """

    def list(self, request):
        # Check cache first
        cached_albums = cache.get("spotify_albums")
        if cached_albums:
            return Response({"albums": cached_albums})

        # Fetch albums from external API
        external_albums = fetch_all_albums()
        if not external_albums:
            return Response({"error": "Failed to fetch albums"}, status=500)

        # Format album data
        albums_data = [
            {
                "id": album.get("id"),
                "name": album.get("name"),
                # "artists": [artist.get("name") for artist in album.get("artists", [])],
                # "release_date": album.get("release_date"),
                # "url": album.get("external_urls", {}).get("spotify"),
                # "album_image": album.get("images", [{}])[0].get("url"),
            }
            for album in external_albums
        ]

        # Cache albums for 15 minutes
        cache.set("spotify_albums", albums_data, timeout=60 * 15)
        return Response({"albums": albums_data})
    

    def retrieve(self, request, pk=None):
        """fetching the details of the each album"""

        #validating the album ID if not then converting the name into the id

        if not re.match(r"^[a-zA-Z0-9]{22}$",pk):
            pk=find_album_by_name(pk)
            if not pk:
                return Response({"error":"Album not found"}, status=404)

        album=fetch_album_by_id(pk)
        if not album:
            return Response({"error": "Failed to fetch album details"}, status=500)

        album_data = {
            "id": album.get("id"),
            "name": album.get("name"),
            "artists": [artist.get("name") for artist in album.get("artists", [])],
            "release_date": album.get("release_date"),
            "url": album.get("external_urls", {}).get("spotify"),
            "album_image": album.get("images", [{}])[0].get("url"),
            "total_tracks": album.get("total_tracks"),
        }

        return Response({"album":album_data})




    @action(detail=True, methods=["get"], url_path="tracks")
    def get_album_tracks(self, request, pk=None):
        # Validate album ID or find by name
        if not re.match(r"^[a-zA-Z0-9]{22}$", pk):
            pk = find_album_by_name(pk)
            if not pk:
                return Response({"error": "Album not found"}, status=404)

        # Fetch tracks for the album
        tracks = fetch_tracks_for_album(pk)
        if not tracks:
            return Response({"error": "Could not fetch tracks"}, status=500)

        # Format track data
        track_data = [
            {
                "name": track.get("name"),
                "track_number": track.get("track_number"),
                "duration_ms": track.get("duration_ms"),
                "url": track.get("external_urls", {}).get("spotify"),
            }
            for track in tracks
        ]

        return Response({"album_id": pk, "tracks": track_data})
    
    




# class RatingViewSet(viewsets.ModelViewSet):
#     """
#     Simplified ViewSet for handling ratings.
#     """
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

