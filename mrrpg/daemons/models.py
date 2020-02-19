from django.db import models

from campaign.models import Campaign
from players.models import Player

class HardpointType(models.Model):
    """
    A type of hardpoint
    """
    name = models.TextField(unique=True)

    def __str__(self) -> str:
        return self.name


class Hardpoint(models.Model):
    """
    Location on a chassis that can hold onto a Mount of some sort
    """
    name = models.TextField(unique=True)

    def __str__(self) -> str:
        return self.location


class Chassis(models.Model):
    """
    A daemon has a chassis underneath it all to describe what
    it can/cannot handle
    """
    name = models.TextField(unique=True)

    hardpoints = models.ManyToManyField(
        Hardpoint,
        through='HardpointConnection'
    )


class HardpointConnection(models.Model):
    """
    Connection that links a chassis to a Hardpoint
    """
    hardpoint = models.ForeignKey(Hardpoint, related_name='connections', on_delete=models.CASCADE)
    chassis = models.ForeignKey(Chassis, related_name='connections', on_delete=models.CASCADE)
    supports = models.ManyToManyField(HardpointType)

    def __str__(self) -> str:
        return (f'{self.chassis.name}: {self.hardpoint.name}('
                f'{s for s in self.supports.all().values_list("name",flat=True)})')


class Item(models.Model):
    """
    A single weapon, shield, AOE, etc.
    """
    name = models.TextField(unique=True)
    type = models.ForeignKey(HardpointType, on_delete=models.PROTECT)
    required_energy = models.IntegerField()

    # -- General JSON blob on information concerning this
    #    item
    _stats = models.TextField()

    def __str__(self) -> str:
        return self.name


    @property
    def stats(self) -> dict:
        return json.loads(self._stats)


    @stats.setter
    def stats(self, value: dict) -> None:
        self._stats = json.dumps(value)



class Daemon(models.Model):
    """
    A daemon instance. This places a Daemon in the world
    """
    chassis = models.ForeignKey(Chassis, on_delete=models.PROTECT)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    name = models.TextField()

    health = models.IntegerField()
    fuel = models.IntegerField()

    mounts = models.ManyToManyField(Item, through='Mount')

    player = models.ForeignKey(
        Player, blank=True, null=True, related_name='daemons', on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        if self.player:
            return f'{self.name}({self.player.player_name or self.player.username})'
        else:
            return f'{self.name}(NPC)'



class Mount(models.Model):
    """
    The connection from a daemons hardpoint to an item
    """
    hardpoint = models.ForeignKey(Hardpoint, on_delete=models.CASCADE)
    daemon = models.ForeignKey(Daemon, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    operational = models.BooleanField(default=True)
    
    # -- Store things like ammo, damage, or other notes
    _stats = models.TextField()

    def __str__(self) -> str:
        return f'{self.daemon} -> {self.item}'


    @property
    def stats(self) -> dict:
        return json.loads(self._stats)


    @stats.setter
    def stats(self, value: dict) -> None:
        self._stats = json.dumps(value)

