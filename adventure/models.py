from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

def connectRooms(base_id, dest_id, direction):
    base = Room.objects.get(id=base_id)
    dest = Room.objects.get(id=dest_id)
    if (not base) or (not dest):
        print("One of the rooms does not exists")
        return
    if direction == "n":
        base.n_to = des.id
        dest.s_to = base.id
    elif direction == "s":
        base.s_to = des.id
        dest.n_to = base.id
    elif direction == "e":
        base.e_to = des.id
        destinationRoom.w_to = base.id
    elif direction == "w":
        base.w_to = des.id
        dest.e_to = base.id
    else:
        print("Invalid direction")
        return
    base.save()
    dest.save()

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            if not hasattr(self, 'id'):
                raise RuntimeError('Not saved yet')
        except Room.DoesNotExist:
            print("That room does not exist")
        except RuntimeError:
            print("Room not saved yet")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
                destinationRoom.s_to = self.id
            elif direction == "s":
                self.s_to = destinationRoomID
                destinationRoom.n_to = self.id
            elif direction == "e":
                self.e_to = destinationRoomID
                destinationRoom.w_to = self.id
            elif direction == "w":
                self.w_to = destinationRoomID
                destinationRoom.e_to = self.id
            else:
                print("Invalid direction")
                return
            self.save()
            destinationRoom.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





