from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location']
    search_fields = ['title'] 

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except Exception as e:
         
            raise e
