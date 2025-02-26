from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
import re
from external_data.services import (
    fetch_all_albums,
    fetch_album_by_id,
    fetch_tracks_for_album,
    fetch_track,
    find_album_by_name,
)
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

# Importing models and serializers
from .models import TrackRating
from .serializers import TrackRatingSerializer, UserSerializer

#user
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class AlbumViewSet(viewsets.ViewSet):
    """
    Simplified ViewSet for fetching albums and their tracks from Spotify API.
    """

    def list(self, request):
        cached_albums = cache.get("spotify_albums")
        if cached_albums:
            return Response({"albums": cached_albums})

        external_albums = fetch_all_albums()
        if not external_albums:
            return Response({"error": "Failed to fetch albums"}, status=500)

        albums_data = [
            {"id": album.get("id"), "name": album.get("name")}
            for album in external_albums
        ]

        cache.set("spotify_albums", albums_data, timeout=60 * 15)
        return Response({"albums": albums_data})

    def retrieve(self, request, pk=None):
        """Fetching the details of each album"""

        if not re.match(r"^[a-zA-Z0-9]{22}$", pk):
            pk = find_album_by_name(pk)
            if not pk:
                return Response({"error": "Album not found"}, status=404)

        album = fetch_album_by_id(pk)
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

        return Response({"album": album_data})

    @action(detail=True, methods=["get"], url_path="tracks")
    def get_album_tracks(self, request, pk=None):
        if not re.match(r"^[a-zA-Z0-9]{22}$", pk):
            pk = find_album_by_name(pk)
            if not pk:
                return Response({"error": "Album not found"}, status=404)

        tracks = fetch_tracks_for_album(pk)
        if not tracks:
            return Response({"error": "Could not fetch tracks"}, status=500)

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

    @action(detail=True, methods=["get"], url_path="tracks/(?P<track_identifier>[^/.]+)")
    def track_details(self, request, pk=None, track_identifier=None):
        """Fetch track details for a specific track in an album"""
        if not re.match(r"^[a-zA-Z0-9]{22}$", pk):
            pk = find_album_by_name(pk)
            if not pk:
                return Response({"error": "Album not found"}, status=404)

        try:
            track_number = int(track_identifier)
            track = fetch_track(pk, track_number=track_number)
        except ValueError:
            if len(track_identifier) == 22:
                track = fetch_track(pk, track_id=track_identifier)
            else:
                track = fetch_track(pk, track_name=track_identifier)

        if not track:
            return Response({"error": f"Track '{track_identifier}' not found in the album"}, status=404)

        track_data = {
            "id": track.get("id"),
            "name": track.get("name"),
            "artists": [artist.get("name") for artist in track.get("artists", [])],
            "url": track.get("external_urls", {}).get("spotify"),
            "duration_ms": track.get("duration_ms"),
            "track_number": track.get("track_number"),
        }

        return Response({"track": track_data}, status=200)


class TrackRatingViewSet(viewsets.ModelViewSet):
    """ViewSet to handle track ratings"""

    queryset = TrackRating.objects.all()
    serializer_class = TrackRatingSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]  # Require authentication

    def create(self, request):
        """Create a new track rating"""

        user = request.user
        data = request.data.copy()
        data["user"] = user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="album/(?P<album_id>[a-zA-Z0-9]{22})")
    def get_album_rating(self, request, album_id=None):
        """Calculate the average rating of the album based on track ratings"""

        avg_rating = TrackRating.objects.filter(album_id=album_id).aggregate(avg=Avg("score"))["avg"]

        if avg_rating is None:
            return Response({"album_id": album_id, "average_rating": "No ratings yet"})

        return Response({"album_id": album_id, "average_rating": round(avg_rating, 2)})


#user registration view
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser



@api_view(['GET']) # Only admin users can access this
def registered_users(request):
    user=User.objects.get(username="uzuw")
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"registered_users": serializer.data})
