from django.contrib.auth.models import User
from adventure.models import Player, Room

import os.path

this_path = os.path.abspath(os.path.dirname(__file__))
rooms_path = os.path.join(this_path, "../../seeds/rooms.json")

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
    print("Creating rooms")
    with open(rooms_path) as json_file:
      data = json.load(json_file)
      rooms = dict()
      for room in data:
        new_room = Room(title=room["title"], description=room["description"])
        new_room.save()
        rooms[room["id"]] = new_room
      for room in data:
        for conn in room["connections"]:
          rooms[room["id"]].connectRooms(rooms[conn["id"]], conn["dir"])

    """
    Example room
      {
        "id": 1,  // Can be a string
        "title": "some_title",
        "description": "some_description",
        "connections": [
          {
            "id": 2, // Can be a string
            "dir": "n"
          }
        ]
      }
    """

    players=Player.objects.all()
    for p in players:
      p.currentRoom=r_outside.id
      p.save()

def run_seed(self):
    """Seed database with rooms"""
    # Clear data from tables
    clear_data()

    create_rooms()