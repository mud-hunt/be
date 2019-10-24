from django.contrib.auth.models import User
from adventure.models import Player, Room

import os.path
import time

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
    print("Deleting room instances...")
    rooms = Room.objects.all()
    rooms.delete()
    print(f"Deleted {len(rooms)} rooms")


def create_rooms():
    """Creates all rooms"""
    print("Creating rooms...")
    start_time = time.time()
    rooms = dict()
    id_map = dict()
    with open(rooms_path) as json_file:
      data = json.load(json_file)
      for room in data:
        new_room = Room(id=room["id"], title=room["title"], description=room["description"])
        new_room.save()
        rooms[room["id"]] = new_room
        id_map[room["id"]] = new_room.id
      for room in data:
        for conn in room["connections"]:
          rooms[room["id"]].connectRooms(rooms[conn["id"]], conn["dir"])
    end_time = time.time()
    print(f"Created {len(rooms)} rooms in {end_time - start_time} seconds")

    """
    Example room
      {
        "id": "start_room",  // Can be a string
        "title": "some_title",
        "description": "some_description",
        "connections": [
          {
            "id": "start_room", // Can be a string
            "dir": "n"
          }
        ]
      }
    """

    start_room = 1
    if 1 in rooms:
      start_room = rooms[1].id
    else:
      start_room = list(rooms.values())[0].id

    print("Resetting player positions")

    players=Player.objects.all()
    for p in players:
      p.currentRoom=start_room
      p.save()
      

def run_seed(self):
    """Seed database with rooms"""
    # Clear data from tables
    clear_data()

    create_rooms()