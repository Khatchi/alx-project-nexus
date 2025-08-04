from django.shortcuts import render
from rest_framework import viewsets, permissions
from movies.models import User
from movies.serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    """
    
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """"""
        return User.objects.filter(user_id=self.request.user.user_id)
    
    def get_object(self):
        """"Return the user object for the current request."""
        return self.request.user
    

