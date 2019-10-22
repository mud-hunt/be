from django.contrib.auth.models import User
from adventure.models import Player, Room

import logging
import json

logger = logging.getLogger(__name__)

# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self)
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete Room instances")
    Room.objects.all().delete()


def create_rooms():
    """Creates all rooms"""
    logger.info("Creating rooms")
    with open('seed.json') as json_file:
      data = json.load(json_file)
      rooms = dict()
      for room in data:
        new_room = Room(title=room.title, description=room.description)
        new_room.save()
        rooms[room.id] = new_room
      for room in data:
        for conn in room.connections:
          rooms[room.id].connectRooms(rooms[conn.id], conn.dir)

    """
    Example room
      {
        "id": 1,
        "title": "some_title",
        "description": "some_description",
        "connections": [
          {
            "id": 2,
            "dir": 'n'
          }
        ]
      }
    """

    r_outside = Room(title="Outside Cave Entrance",
                  description="North of you, the cave mount beckons")

    r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
    passages run north and east.""")

    r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
    into the darkness. Ahead to the north, a light flickers in
    the distance, but there is no way across the chasm.""")

    r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
    to north. The smell of gold permeates the air.""")

    r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
    chamber! Sadly, it has already been completely emptied by
    earlier adventurers. The only exit is to the south.""")

    r_test = Room(title="Test room", description="""You've found the long-lost treasure
    chamber! Sadly, it has already been completely emptied by
    earlier adventurers. The only exit is to the south.""")

    players=Player.objects.all()
    for p in players:
      p.currentRoom=r_outside.id
      p.save()

def run_seed(self):
    """Seed database with rooms"""
    # Clear data from tables
    clear_data()

    create_rooms()