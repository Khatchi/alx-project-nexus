import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True, blank=False, null=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    preferences = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        """returns a string representation of the user."""
        return f"User: {self.username} (ID: {self.user_id})"\
            if self.username else "User: Anonymous"
    
    class Meta:
        """Meta options for the User model."""

        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
        ]


class Movie(models.Model):
    """
    Model representing movies from the TMDB API.
    """

    movie_id = models.IntegerField(primary_key=True)

    title = models.CharField(max_length=255)

    release_year = models.IntegerField()

    overview = models.TextField(blank=True)  

    poster_path = models.CharField(max_length=255, blank=True)

    genres = models.JSONField(default=list)

    average_rating = models.FloatField(default=0.0)

    popularity = models.FloatField(default=0.0)

    cached_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        """returns a string representation of the movie."""
        return f"{self.title} ({self.release_year})"
    
    class Meta:
        """Meta options for the movie model."""

        ordering = ['-release_year']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_year']),
        ]