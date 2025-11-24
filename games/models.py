from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

class Game(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

@receiver(pre_delete, sender=Game)
def prevent_game_delete_with_scores(sender, instance, **kwargs):
    if instance.score_set.exists():
        raise ValidationError(
            {"error": "Cannot delete game with existing scores. Tournament has active games."}
        )