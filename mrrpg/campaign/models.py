from django.db import models


class Campaign(models.Model):
    """
    A campaign hosts a set of players, npcs, maps, and more!
    """
    name = models.TextField(unique=True)

    def __str__(self) -> str:
        return self.name
