from django.urls import path
from .views import (
    GameLeaderboardView, 
    TopPlayersLeaderboardView, 
    GlobalRatingLeaderboardView
)

urlpatterns = [
    path('leaderboard/', GameLeaderboardView.as_view(), name='game-leaderboard'),
    path('leaderboard/top/', TopPlayersLeaderboardView.as_view(), name='top-players-leaderboard'),
    path('leaderboard/global/', GlobalRatingLeaderboardView.as_view(), name='global-rating-leaderboard'),
]