from django.test import TestCase

from campaign.models import Campaign
from players.models import Player

from .models import (
    Chassis,
    HardpointType,
    HardpointConnection,
    Hardpoint,
    Item,
    Daemon,
    Mount
)


class TestDaemons(TestCase):
    """
    Test creating Daemon objects
    """
    def setUp(self):
        """
        Build some default types
        """
        names = [
            'ballistic',
            'laser',
            'missile',
            'shield',
            'engine',
            'aoe',
            'core'
        ]

        self.hp_types = {}
        for name in names:
            self.hp_types[name] = HardpointType.objects.create(
                name=name
            )

        default_hardpoint_names = [
            'left arm',
            'right arm',
            'left shoulder',
            'right shoulder',
            'core',
            'engine'
        ]

        self.hardpoints = {}
        for hpn in default_hardpoint_names:
            self.hardpoints[hpn] = Hardpoint.objects.create(
                name=hpn
            )

        some_items = {

            # -- Weapons

            # ballistic
            'TR16 (Recruit)': ('ballistic', 2, {'dmg': '1d6', 'acc': 1, 'base_cost': 120}),
            'YF88': ('ballistic', 3, {'dmg': '1d6+2', 'acc': 2, 'base_cost': 250}),

            # laser 
            'XD-452': ('laser', 3, {'dmg': '1d4', 'acc': 3, 'base_cost': 195}),
            'QY-9999 (Exterminator)': ('laser', 16, {'dmg': '2d20+10', 'acc': 14, 'base_cost': 525000}),

            # Missile
            'TB_009': ('missile', 6, {'dmg': '1d8', 'acc': 3, 'base_cost': 270}),
            'Terrus Missile Battery': ('missile', 8, {'dmg': '2d6', 'acc': 4, 'base_cost': 2200}),

            # -- Shields
            'SI Ballistic Shield': ('shield', 1, {'block': 3, 'coverage': 2, 'base_cost': 130}),
            'TiS Tower Shield': ('shield', 2, {'block': 4, 'coverage': 3, 'base_cost': 240}),

            # -- Engines
            'SI Recruit Engine': ('engine', 4, {'movement': 2, 'base_cost': 130}),
            'TiS Outlander Engine': ('engine', 7, {'movement': 4, 'base_cost': 500}),

            # -- AOE
            'Dell Power Grid': ('aoe', 4, {'type': 'energy', 'range': 3, 'base_cost': 400}),
            'Titian Kinetic Shield': ('aoe', 7, {'type': 'k-shield', 'range': 4, 'base_cost': 970}),

            # -- Cores
            'SI Recruit Core': ('core', -15, {'heat_limit': 4, 'base_cost': 100}),
            'TiS Outlander Core': ('core', -25, {'heat_limit': 7, 'base_cost': 10000}),
        }
        self.items = {}
        for name, data in some_items.items():
            self.items[name] = Item.objects.create(
                name=name,
                type=self.hp_types[data[0]],
                required_energy=data[1],
                _stats=data[2]
            )


    def test_make_basics(self):
        """
        Make some basic objects
        """

        # -- BASICS
        chassis = Chassis.objects.create(
            name='recruit'
        )
        connection = HardpointConnection.objects.create(
            hardpoint=self.hardpoints['left arm'],
            chassis=chassis
        )
        connection.supports.set([self.hp_types['ballistic']])


        # -- CAMPAIGN
        campaign = Campaign.objects.create(
            name='The Great Journey'
        )

        player = Player.objects.create(username='dave')

        daemon = Daemon.objects.create(
            chassis=chassis,
            campaign=campaign,
            name='WhiteGhost',
            health=12,
            fuel=15,
            player=player
        )

        mount = Mount.objects.create(
            hardpoint=connection.hardpoint,
            daemon=daemon,
            item=self.items['TR16 (Recruit)'],
            operational=True,
            _stats={}
        )

        print (Mount.objects.filter(daemon=daemon))
