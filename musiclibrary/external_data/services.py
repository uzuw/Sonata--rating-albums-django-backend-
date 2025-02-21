import requests
import base64
from django.core.cache import cache
from django.conf import settings

def get_spotify_access_token():
    """
    Fetch a Spotify access token using client credentials.
    """
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    auth_url = "https://accounts.spotify.com/api/token"

    # Encode client ID and secret for authentication
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # Request access token
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get Spotify token: {response.json().get('error_description', 'Unknown error')}")

    return response.json()["access_token"]

def fetch_all_albums():
    """
    Fetch new release albums from Spotify and cache the results.
    """
    # Check if the access token is cached
    access_token = cache.get("spotify_access_token")
    if not access_token:
        access_token = get_spotify_access_token()
        cache.set("spotify_access_token", access_token, timeout=3600)  # Cache token for 1 hour

    # Fetch new releases from Spotify
    url = "https://api.spotify.com/v1/browse/new-releases?limit=50"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        albums = response.json().get("albums", {}).get("items", [])
        cache.set("spotify_all_albums", albums, timeout=3600)  # Cache albums for 1 hour
        return albums

    return None