from .serializers import ScoreCreateSerializer, ScoreRetrieveSerializer 
from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Score
from .filters import ScoreFilter


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ScoreFilter
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScoreCreateSerializer 
        elif self.action in ('list', 'retrieve'):
            return ScoreRetrieveSerializer 
        return ScoreCreateSerializer