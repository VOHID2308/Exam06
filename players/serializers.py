from rest_framework import serializers
from .models import Player

class PlayerStatsMixin(serializers.Serializer):
    """Playerning partiyalar statistikasi uchun mixin"""
    total_games = serializers.IntegerField(read_only=True)
    wins = serializers.IntegerField(read_only=True)
    draws = serializers.IntegerField(read_only=True)
    losses = serializers.IntegerField(read_only=True)

class PlayerSerializer(PlayerStatsMixin, serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ('rating', 'created_at') 


class PlayerRetrieveSerializer(PlayerSerializer):
    """Retrieve uchun to'liq statistika bilan"""
    pass 