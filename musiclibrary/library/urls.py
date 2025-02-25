from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, TrackRatingViewSet, RegisterUserView, registered_users



router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename="album")
# router.register(r'ratings', RatingViewSet, basename="rating")
router.register(r'track-ratings', TrackRatingViewSet, basename="track-ratings")




#Authentication endpoints


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#TokenObtainPreview
#its used to generate a pair of JWT tokens:
# ACCESS TOKEN with very short life span and REFRESH TOKEN with longer lifespan


#TokenRefreshView
#used to refresh an expired access token

#OAuth2 can be used to have vaster token management




urlpatterns = [
    path('api/', include(router.urls)),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/users/', registered_users, name='registered-users'),
]


