from django.http import JsonResponse
from django.core.cache import cache
from .services import fetch_all_albums

def get_all_albums(request):
    """API endpoint to fetch all available albums from Spotify."""
    cached_albums = cache.get("spotify_all_albums")
    if cached_albums:
        return JsonResponse({"albums": cached_albums})

    albums = fetch_all_albums()
    if albums:
        return JsonResponse({"albums": albums})
    
    return JsonResponse({"error": "Could not fetch albums"}, status=500)


