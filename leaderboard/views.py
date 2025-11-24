from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Case, When, IntegerField, F
from players.models import Player
from games.models import Game
from scores.models import Score
from .serializers import (
    GameLeaderboardSerializer, 
    TopPlayersLeaderboardSerializer, 
    GlobalLeaderboardPlayerSerializer
)

def get_game_leaderboard_data(game_id):
    """Game (Turnir) Leaderboard uchun asosiy mantig'i"""
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return None

    leaderboard_data = Score.objects.filter(game_id=game_id).values('player').annotate(
        wins=Count(Case(When(result='win', then=1), output_field=IntegerField())),
        draws=Count(Case(When(result='draw', then=1), output_field=IntegerField())),
        losses=Count(Case(When(result='loss', then=1), output_field=IntegerField())),
        points=Sum(Case(
            When(result='win', then=10),
            When(result='draw', then=5),
            default=0,
            output_field=IntegerField()
        ))
    ).order_by('-points')

    results = []
    
    for rank, data in enumerate(leaderboard_data, 1):
        player_id = data['player']
        player = Player.objects.get(id=player_id)
        
        player_scores = Score.objects.filter(player_id=player_id, game_id=game_id).order_by('created_at', 'id')
        
       
        initial_rating = player_scores.first().points if player_scores.exists() and player_scores.first().points is not None else player.rating - data['points'] 
        
        final_rating = player.rating

        result = {
            'rank': rank,
            'player__nickname': player.nickname,
            'player__id': player.id,
            'player__country': player.country,
            'rating': final_rating,
            'points': data['points'],
            'wins': data['wins'],
            'draws': data['draws'],
            'losses': data['losses'],
            'rating_change': final_rating - initial_rating,
        }
        results.append(result)

    return results

class GameLeaderboardView(APIView):
    """GET /api/leaderboard/?game_id={id}"""
    def get(self, request):
        game_id = request.query_params.get('game_id')
        if not game_id:
            return Response({"error": "game_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        leaderboard_data = get_game_leaderboard_data(game_id)
        if leaderboard_data is None:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameLeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopPlayersLeaderboardView(APIView):
    """GET /api/leaderboard/top/?game_id={id}&limit={n}"""
    def get(self, request):
        game_id = request.query_params.get('game_id')
        limit = request.query_params.get('limit', 10)
        
        try:
            limit = int(limit)
        except ValueError:
            return Response({"error": "limit must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        limit = max(1, min(limit, 50))

        if not game_id:
            return Response({"error": "game_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        leaderboard_data = get_game_leaderboard_data(game_id)
        if leaderboard_data is None:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)
        
        total_players = len(leaderboard_data)
        top_players = leaderboard_data[:limit]

        serializer = TopPlayersLeaderboardSerializer(top_players, many=True)
        
        response_data = {
            "game_id": game.id,
            "game_title": game.title,
            "limit": limit,
            "total_players": total_players,
            "leaderboard": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class GlobalRatingLeaderboardView(APIView):
    """GET /api/leaderboard/global/"""
    def get(self, request):
        country = request.query_params.get('country')
        limit = request.query_params.get('limit', 100)

        try:
            limit = int(limit)
        except ValueError:
            return Response({"error": "limit must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        limit = max(1, min(limit, 500))

        queryset = Player.objects.all()

        if country:
            queryset = queryset.filter(country__iexact=country)

        queryset = queryset.annotate(
            total_games=Count('score')
        ).order_by('-rating')

        total_players = queryset.count()
        leaderboard_data = queryset[:limit]

        results = []
        for rank, player in enumerate(leaderboard_data, 1):
            player.rank = rank
            results.append(player)

        serializer = GlobalLeaderboardPlayerSerializer(results, many=True)
        
        response_data = {
            "total_players": total_players,
            "country": country if country else "All",
            "leaderboard": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)