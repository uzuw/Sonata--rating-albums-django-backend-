from rest_framework import viewsets
from rest_framework.response import Response
from .models import Album, Track, Rating
from .serializers import AlbumSerializer, TrackSerializer, RatingSerializer
from external_data.services import fetch_all_albums

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def list(self, request, *args, **kwargs):
        external_albums = fetch_all_albums()

        # Ensure it's a list of albums
        albums_data = [
            {
                "name": album.get("name"),
                "album_type": album.get("album_type"),
                "artists": [artist.get("name") for artist in album.get("artists", [])],
                "release_date": album.get("release_date"),
                "total_tracks": album.get("total_tracks"),
                "href": album.get("href"),
                "url": album.get("external_urls", {}).get("spotify"),
            }
            for album in external_albums
        ]

        return Response({"external_albums": albums_data})
 



class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
