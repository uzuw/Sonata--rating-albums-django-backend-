from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, TrackRatingViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename="album")
# router.register(r'ratings', RatingViewSet, basename="rating")
router.register(r'track-ratings', TrackRatingViewSet, basename="track-ratings")


urlpatterns = [
    path('api/', include(router.urls)),  
]
