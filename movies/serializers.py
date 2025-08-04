from rest_framework import serializers
from movies.models import User, Movie, Rating, Watchlist, TrendingMovie, Recommendation

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        """Meta options for the UserSerializer."""

        model = User

        fields = [
            'user_id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'preferences',
            'is_active',
            'date_joined',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['user_id', 'date_joined', 'created_at', 'updated_at']



class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """

    class Meta:
        """Meta options for the MovieSerializer."""

        model = Movie

        fields = [
            'movie_id',
            'title', 
            'release_year',
            'overview',
            'poster_path',
            'genres',
            'average_rating',
            'popularity',
            'cached_at'
        ]
        read_only_fields = ['cached_at']


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model.
    """

    class Meta:
        """Meta options for the RatingSerializer."""

        model = Rating

        fields = [
            'id',
            'user',
            'tmdb_id',
            'rating',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class WatchlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the Watchlist model.
    """

    class Meta:
        """Meta options for the WatchlistSerializer."""

        model = Watchlist

        fields = [
            'id',
            'user',
            'tmdb_id',
            'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class TrendingMovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrendingMovie model.
    """

    class Meta:
        """Meta options for the TrendingMovieSerializer."""

        model = TrendingMovie
        
        fields = [
            'tmdb_id',
            'title',
            'popularity',
            'cached_at'
        ]
        read_only_fields = ['cached_at']


class RecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recommendation model.
    """

    movie = MovieSerializer(source='tmdb_id', read_only=True)
    
    class Meta:
        """Meta options for the RecommendationSerializer."""

        model = Recommendation

        fields = [
            'id',
            'user',
            'tmdb_id',
            'score',
            'generated_at',
            'movie'
        ]

        read_only_fields = ['generated_at', 'movie']