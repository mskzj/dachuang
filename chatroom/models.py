from django.db import models
from account.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room_name = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    person_num = models.IntegerField(default=0)
    person_max = models.IntegerField(default=20)

class Persons(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    room_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)