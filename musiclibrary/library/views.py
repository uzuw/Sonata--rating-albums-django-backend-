# we import the models and their serialized data here

from rest_framework import viewsets, permissions

#viewsets for abstraction/ for hadeling different HTTP methods
#permissions in DRF control access to api end points

from .models import Album, Track, Rating
from .serializers import AlbumSerializer, TrackSerializer, RatingSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset=Album.objects.all()
    serializer_class= AlbumSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class TrackViewSet(viewsets.ModelViewSet):
    queryset= Track.objects.all()
    serializer_class=AlbumSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class RatingViewSet(viewsets.ModelViewSet):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer
    permission_classes=[permissions.IsAuthenticated]
    