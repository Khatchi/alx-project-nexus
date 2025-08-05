from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.views import MovieViewSet, RatingViewSet, UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]