import requests
import base64
from django.core.cache import cache
from django.conf import settings

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1/albums"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"

def get_spotify_access_token():
    """
    Fetch a Spotify access token using client credentials and cache it.
    """
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    # Encode client ID and secret for authentication
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    # Request access token
    response = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(
            f"Failed to get Spotify token: {response.json().get('error_description', 'Unknown error')}"
        )

    token_data = response.json()
    access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour

    # Cache token for its valid duration
    cache.set("spotify_access_token", access_token, timeout=expires_in - 60)  # 1 min buffer
    return access_token


def fetch_all_albums():
    """
    Fetch new release albums from Spotify and cache the results.
    """
    # Get or refresh access token
    access_token = cache.get("spotify_access_token")
    if not access_token:
        access_token = get_spotify_access_token()

    # Fetch new releases from Spotify
    url = "https://api.spotify.com/v1/browse/new-releases?limit=50"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        albums = response.json().get("albums", {}).get("items", [])
        cache.set("spotify_all_albums", albums, timeout=3600)  # Cache albums for 1 hour
        return albums

    return None


def fetch_album_by_id(album_id):
    """
    Fetch details of a specific album by its Spotify ID.
    """
    access_token = cache.get("spotify_access_token") or get_spotify_access_token()
    if not access_token:
        return None

    url = f"{SPOTIFY_API_BASE_URL}/{album_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()

    return None


def fetch_tracks_for_album(album_id):
    """
    Fetch tracks for a specific album using its Spotify Album ID.
    """
    # Get or refresh access token
    access_token = cache.get("spotify_access_token") or get_spotify_access_token()
    if not access_token:
        access_token = get_spotify_access_token()

    url = f"{SPOTIFY_API_BASE_URL}/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}  # Added "Bearer "

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("items", [])

    return None


def find_album_by_name(album_name):
    """Searches for an album on Spotify and return its ID"""

    access_token = cache.get("spotify_access_token") or get_spotify_access_token()
    url = f"{SPOTIFY_SEARCH_URL}?q={album_name}&type=album&limit=1"
    headers = {"Authorization": f"Bearer {access_token}"}

    response=requests.get(url, headers=headers)

    if response.status_code==200:
        albums=response.json().get("albums",{}).get("items",[])
        if albums:
            return albums[0]['id'] #returning the id using the name of the album
        


