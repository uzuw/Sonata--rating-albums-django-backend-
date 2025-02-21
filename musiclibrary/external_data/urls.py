from django.urls import path
from .views import get_all_albums

urlpatterns = [
    path('albums/', get_all_albums, name="get_all_albums"),
]
