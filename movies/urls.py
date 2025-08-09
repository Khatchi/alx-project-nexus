from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.views import MovieViewSet, RatingViewSet, RecommendationViewSet, TrendingMovieViewSet, UserViewSet, WatchlistViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'trending', TrendingMovieViewSet, basename='trending')
router.register(r'recommendations', TrendingMovieViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]