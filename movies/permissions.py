from rest_framework.permissions import BasePermission


class IsAuthenticatedOrReadOnlyForMovies(BasePermission):
    """
    Allow authenticated users full access, anonymous users read-only.
    Perfect for movie browsing where you want logged-in users to have more features.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only for authenticated users
        return request.user and request.user.is_authenticated


class MovieAccessPermission(BasePermission):
    """
    Custom permission for movie access with different levels:
    - Anonymous: Can view trending and discover movies only
    - Authenticated: Full access to all movie endpoints
    """
    
    def has_permission(self, request, view):
        # Always allow GET requests
        if request.method != 'GET':
            return False
            
        # For anonymous users, only allow trending and discover
        if not request.user.is_authenticated:
            return view.action in ['trending', 'discover', 'list']
        
        # Authenticated users get full access
        return True