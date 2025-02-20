from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import AlbumViewSet, TrackViewSet, RatingViewSet


#making routes

router=DefaultRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'tracks',TrackViewSet)
router.register(r'ratings', RatingViewSet)


urlpatterns=[

path('api/',include(router.urls)), # links to router

]