from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
import requests
import logging
from movies.models import Movie, Rating, User
from movies.serializers import MovieSerializer, RatingSerializer, UserSerializer
from movies.tmdb import TMDbAPI

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    - Allows users to retrieve their own profile information.
    - Uses UserSerializer to serialize user data.
    - Only allows authenticated users to access their own data.
    - Provides a custom get_object method to return the current user.
    - Uses Django's built-in permissions to restrict access.
    - Supports listing all users, but typically restricted to admin users.
    - Uses ModelViewSet for CRUD operations on User model.
    """
    
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """"""
        return User.objects.filter(user_id=self.request.user.user_id)
    
    def get_object(self):
        """"Return the user object for the current request."""
        return self.request.user


# Set up logging
logger = logging.getLogger(__name__)

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing movies fetched from TMDb.
    - Uses TMDb ID as the lookup field
    - Automatically caches movie details for 24 hours
    - Handles all TMDb API interactions transparently
    """
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'tmdb_id'
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        """
        Retrieve a movie by TMDb ID, fetching from TMDb API if not cached.
        Overrides default get_object to implement custom caching logic.
        """
        tmdb_id = self.kwargs.get('tmdb_id')
        
        try:
            tmdb_id = int(tmdb_id)
        except (ValueError, TypeError):
            logger.error(f"Invalid TMDb ID format: {tmdb_id}")
            raise status.HTTP_404_NOT_FOUND("Invalid TMDb ID format")

        try:
            # Check for cached version (less than 24 hours old)
            cache_threshold = timezone.now() - timedelta(hours=24)
            movie = Movie.objects.filter(
                tmdb_id=tmdb_id, 
                cached_at__gte=cache_threshold
            ).first()

            if not movie:
                # Fetch from TMDb API if not cached or cache expired
                tmdb_data = TMDbAPI.get_movie_details(tmdb_id)
                
                if not tmdb_data.get('genres'):
                    logger.error(f"No genres found for movie {tmdb_id}")
                    raise status.HTTP_404_NOT_FOUND("No genres found for this movie")

                # Update or create the movie record
                movie, created = Movie.objects.update_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        'title': tmdb_data.get('title', ''),
                        'release_year': self._extract_year(tmdb_data.get('release_date')),
                        'overview': tmdb_data.get('overview', ''),
                        'poster_path': tmdb_data.get('poster_path', ''),
                        'genres': [g['name'] for g in tmdb_data.get('genres', [])],
                        'popularity': tmdb_data.get('popularity', 0.0),
                        'cached_at': timezone.now(),
                    }
                )
                logger.info(f"{'Created' if created else 'Updated'} movie: {movie.title}")

            return movie

        except requests.RequestException as e:
            logger.error(f"TMDb API error for movie {tmdb_id}: {str(e)}")
            raise status.HTTP_404_NOT_FOUND("Failed to fetch movie data from TMDb")
        except Exception as e:
            logger.error(f"Unexpected error retrieving movie {tmdb_id}: {str(e)}")
            raise status.HTTP_404_NOT_FOUND("Internal server error")

    def _extract_year(self, release_date):
        """Helper method to extract year from release date string."""
        if not release_date:
            return None
        try:
            return int(release_date[:4])
        except (ValueError, TypeError):
            return None

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending movies from TMDb."""
        try:
            time_window = request.query_params.get('time_window', 'day')
            if time_window not in ['day', 'week']:
                time_window = 'day'

            movies_data = TMDbAPI.get_trending_movies(time_window)
            
            # Store trending movies in database for caching
            movies = []
            for movie_data in movies_data[:20]:  # Limit to 20 movies
                movie, _ = Movie.objects.update_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title', ''),
                        'release_year': self._extract_year(movie_data.get('release_date')),
                        'overview': movie_data.get('overview', ''),
                        'poster_path': movie_data.get('poster_path', ''),
                        'popularity': movie_data.get('popularity', 0.0),
                        'cached_at': timezone.now(),
                    }
                )
                movies.append(movie)

            serializer = self.get_serializer(movies, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error fetching trending movies: {str(e)}")
            return Response(
                {'error': 'Failed to fetch trending movies'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=False, methods=['get'])
    def discover(self, request):
        """Discover movies by genre from TMDb."""
        try:
            genre_ids = request.query_params.get('genres')
            if genre_ids:
                try:
                    genre_ids = [int(x.strip()) for x in genre_ids.split(',')]
                except ValueError:
                    return Response(
                        {'error': 'Invalid genre IDs format'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                genre_ids = None

            movies_data = TMDbAPI.discover_movies(genre_ids)
            
            # Store discovered movies in database
            movies = []
            for movie_data in movies_data[:20]:  # Limit to 20 movies
                movie, _ = Movie.objects.update_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title', ''),
                        'release_year': self._extract_year(movie_data.get('release_date')),
                        'overview': movie_data.get('overview', ''),
                        'poster_path': movie_data.get('poster_path', ''),
                        'popularity': movie_data.get('popularity', 0.0),
                        'cached_at': timezone.now(),
                    }
                )
                movies.append(movie)

            serializer = self.get_serializer(movies, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error discovering movies: {str(e)}")
            return Response(
                {'error': 'Failed to discover movies'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def list(self, request):
        """List all cached movies with pagination."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Disable direct movie creation."""
        return Response(
            {'error': 'Direct movie creation not allowed. Use TMDb ID to fetch movies.'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        """Disable movie updates."""
        return Response(
            {'error': 'Movie updates not allowed. Data is fetched from TMDb.'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        """Allow deletion of cached movies."""
        return super().destroy(request, *args, **kwargs)



class RatingViewSet(viewsets.ModelViewSet):
    """Viewset for managing movie ratings.
    - Allows users to create, retrieve, update, and delete ratings.
    - Automatically calculates and updates the average rating for movies.
    - Uses RatingSerializer to serialize rating data.
    - Requires user authentication for all actions.
    - Supports listing all ratings, but typically restricted to admin users.
    - Uses ModelViewSet for CRUD operations on Rating model.
    """

    queryset = Rating.objects.all()
    
    serializer_class = RatingSerializer
  

    def perform_create(self, serializer):
        """Override to set the user automatically when creating a rating."""
        serializer.save(user=self.request.user)
        # Update average rating
        tmdb_id = serializer.validated_data['tmdb_id']
        avg_rating = Rating.objects.filter(tmdb_id=tmdb_id).aggregate(Avg('rating'))['rating__avg'] or 0.0
        Movie.objects.filter(tmdb_id=tmdb_id).update(average_rating=avg_rating)