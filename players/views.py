from django.shortcuts import render
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Count, Case, When, IntegerField
from .models import Player
from .serializers import PlayerSerializer, PlayerRetrieveSerializer
from .filters import PlayerFilter

class PlayerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Player.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PlayerFilter
    search_fields = ['nickname']

    def get_queryset(self):
        
        queryset = super().get_queryset().annotate(
            total_games=Count('score'),
            wins=Count(Case(When(score__result='win', then=1), output_field=IntegerField())),
            draws=Count(Case(When(score__result='draw', then=1), output_field=IntegerField())),
            losses=Count(Case(When(score__result='loss', then=1), output_field=IntegerField()))
        )
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PlayerRetrieveSerializer
        return PlayerSerializer

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except Exception as e:
          
            raise e
