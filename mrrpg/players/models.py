from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    """
    A single player.
    """
    player_name = models.TextField(null=True, blank=True)
