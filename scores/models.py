from django.db import models
from players.models import Player
from games.models import Game
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

RESULT_CHOICES = (
    ('win', 'G\'alaba'),
    ('loss', 'Mag\'lubiyat'),
    ('draw', 'Durang'),
)


def calculate_new_rating(player_id):
    from players.models import Player 
    from django.db.models import Sum, Case, When, Value, IntegerField
    
    player = Player.objects.get(id=player_id)
    
    current_rating = 0
    
    scores = Score.objects.filter(player_id=player_id)

    total_points = scores.aggregate(
        sum_points=Sum(
            Case(
                When(result='win', then=Value(10)),
                When(result='draw', then=Value(5)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
    )['sum_points'] or 0

    new_rating = total_points
    
    player.rating = new_rating
    player.save()

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    points = models.IntegerField(null=True, blank=True) 
    opponent_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

@receiver(post_save, sender=Score)
def update_player_rating_on_score_save(sender, instance, created, **kwargs):
    if created:
        calculate_new_rating(instance.player.id)
    else:
     
        pass

@receiver(post_delete, sender=Score)
def update_player_rating_on_score_delete(sender, instance, **kwargs):
    calculate_new_rating(instance.player.id, instance.id)
