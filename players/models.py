from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

@receiver(pre_delete, sender=Player)
def prevent_player_delete_with_scores(sender, instance, **kwargs):
    game_count = instance.score_set.count()
    if game_count > 0:
        raise ValidationError(
            {"error": f"Cannot delete player with game history. Player has {game_count} recorded games."}
        )