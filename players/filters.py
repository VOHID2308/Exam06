import django_filters
from .models import Player

class PlayerFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')

    class Meta:
        model = Player
        fields = ['country', 'min_rating']