from rest_framework import serializers
from .models import Score, RESULT_CHOICES
from games.models import Game
from players.models import Player

class NestedGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title')

class NestedPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'nickname')

class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('game', 'player', 'result', 'opponent_name')

    def validate_result(self, value):
        if value not in dict(RESULT_CHOICES).keys():
            raise serializers.ValidationError(f"Invalid result value. Must be one of: {list(dict(RESULT_CHOICES).keys())}")
        return value

class ScoreRetrieveSerializer(serializers.ModelSerializer):
    game = NestedGameSerializer(read_only=True)
    player = NestedPlayerSerializer(read_only=True)
    
    points = serializers.SerializerMethodField() 

    def get_points(self, obj):
        if obj.result == 'win':
            return 10
        elif obj.result == 'draw':
            return 5
        return 0

    class Meta:
        model = Score
        fields = ('id', 'game', 'player', 'result', 'points', 'opponent_name', 'created_at')
        read_only_fields = fields 