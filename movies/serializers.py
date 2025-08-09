from rest_framework import serializers
from movies.models import User, Movie, Rating, Watchlist, Recommendation

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    password = serializers.CharField(write_only=True, min_length=8)
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

        extra_kwargs = {
            'password': {'write_only': True} 
        }

    # methods to handle password hashing

    def create(self, validated_data):
        """Create user with hashed password"""
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update user and hash password if provided"""
        password = validated_data.pop('password', None)
        
        # Update other fields
        instance = super().update(instance, validated_data)
        
        # Hash and set password if provided
        if password:
            instance.set_password(password)
            instance.save()
        
        return instance



class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """

    class Meta:
        """Meta options for the MovieSerializer."""

        model = Movie

        fields = [
            'tmdb_id',
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


class RecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recommendation model.
    """

    class Meta:
        """Meta options for the RecommendationSerializer."""

        model = Recommendation

        fields = [
            'tmdb_id',
            'title',
            'popularity',
            'cached_at'
        ]
        read_only_fields = ['cached_at']