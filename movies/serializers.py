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
        