import requests
from django.conf import settings
from django.core.cache import cache
from datetime import timedelta


class TMDbAPI:
    """
    Class to interact with The Movie Database (TMDb) API.

    - Provides methods to fetch movie details, trending movies, and discover movies based on genres.
    - Caches results for 24 hours to reduce API calls and improve performance.
    - Uses Django's cache framework to store results.
    - Requires TMDb API key to be set in Django settings.
    """

    # def __init__(self):
    #     self.access_token = settings.TMDB_API_KEY
    #     self.base_url = "https://api.themoviedb.org/3/"

    BASE_URL = "https://api.themoviedb.org/3"
    CACHE_TIMEOUT = timedelta(hours=24).total_seconds()


    @staticmethod
    def get_movie_details(tmdb_id):
        """
        Fetch movie details from TMDb API.
        """
        cache_key = f"movie_{tmdb_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        

        url = f"{TMDbAPI.BASE_URL}/movie/{tmdb_id}"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        cache.set(cache_key, data, TMDbAPI.CACHE_TIMEOUT)
        return data
    

    
    @staticmethod
    def get_trending_movies(time_window='day'):
        """
        Fetch trending movies from TMDb API.
        """

        cache_key = f"trending_{time_window}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        

        url = f"{TMDbAPI.BASE_URL}/trending/movie/{time_window}"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['results']
        cache.set(cache_key, data, TMDbAPI.CACHE_TIMEOUT)
        return data


    @staticmethod
    def discover_movies(genre_ids=None):
        """Discover movies based on genre IDs."""

        cache_key = f"discover_genres_{genre_ids}" if genre_ids else "discover_all"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        url = f"{TMDbAPI.BASE_URL}/discover/movie"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US',
        }

        if genre_ids:
            params['with_genres'] = ','.join(map(str, genre_ids))
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['results']
        cache.set(cache_key, data, TMDbAPI.CACHE_TIMEOUT)
        return data