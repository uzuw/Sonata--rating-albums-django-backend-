from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename="album")
router.register(r'ratings', RatingViewSet, basename="rating")

urlpatterns = [
    path('api/', include(router.urls)),  
]
