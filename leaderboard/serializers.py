from rest_framework import serializers
from players.models import Player
from games.models import Game
from scores.models import Score

class GameLeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField(read_only=True)
    player = serializers.CharField(source='player__nickname', read_only=True)
    player_id = serializers.IntegerField(source='player__id', read_only=True)
    country = serializers.CharField(source='player__country', read_only=True)
    rating = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)
    rating_change = serializers.IntegerField(read_only=True)

class TopPlayersLeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField(read_only=True)
    player = serializers.CharField(source='player__nickname', read_only=True)
    country = serializers.CharField(source='player__country', read_only=True)
    rating = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)

class GlobalLeaderboardPlayerSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField(read_only=True)
    player = serializers.CharField(source='nickname', read_only=True)
    total_games = serializers.IntegerField(read_only=True)

    class Meta:
        model = Player
        fields = ('rank', 'player', 'rating', 'total_games')