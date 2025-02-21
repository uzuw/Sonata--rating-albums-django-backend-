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
        local_albums = AlbumSerializer(self.get_queryset(), many=True).data
        return Response({"local_albums": local_albums, "external_albums": external_albums})

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
