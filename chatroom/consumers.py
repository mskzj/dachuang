import json
import datetime
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chatroom.models import Room,Persons
from account.models import User,Userinfo

@database_sync_to_async
def get_user(session):
    username = session.get('username', default=None)
    if username:
        user = User.objects.get(username=username)
        userinfo = Userinfo.objects.get(user=user)
        # print(userinfo.nickname)
        return userinfo.nickname,userinfo.headimg.url


@database_sync_to_async
def add_room(room_name,session):
    username = session.get('username', default=None)
    if username:
        user = User.objects.get(username=username)
        room = Room.objects.get(room_name=room_name)
        if Persons.objects.filter(room_user=user,room=room):
            print("----------{0}该用户已经在聊天室中-------".format(username))
        else:
            # 房间人数加1
            room.person_num += 1  # 房间人数加1
            room.save()
            #加入聊天室
            person = Persons(room_user=user, room=room)
            person.save()


@database_sync_to_async
def sub_room(room_name,session):
    username = session.get('username', default=None)
    if username:
        user = User.objects.get(username=username)
        room = Room.objects.get(room_name=room_name)
        if Persons.objects.filter(room_user=user,room=room):
            # 房间人数-1
            room.person_num -= 1  # 房间人数加1
            room.save()
            print("okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            if room.person_num == 0:  #如果房间无人则删除房间
                room.delete()
            person = Persons.objects.get(room_user=user, room=room)
            person.delete()


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         #user =  text_data_json['user']
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#             #    'user': 'user',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         # user  = event['user']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#         #    'user': 'user',
#             'message': message
#         }))

# class ChatConsumer2(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#
#         self.room_group_name = 'chat_%s' % self.room_name
#         self.session = self.scope["session"]
#
#         await  add_room(self.room_name,self.session)
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         self.session = self.scope["session"]
#
#         await  sub_room(self.room_name,self.session)
#
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         #user =  text_data_json['user']
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#             #    'user': 'user',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         # user  = event['user']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#         #    'user': 'user',
#             'message': message
#         }))

class ChatConsumer3(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'chat_%s' % self.room_name
        self.session = self.scope["session"]
        self.userinfo = await get_user(self.session)

        await  add_room(self.room_name,self.session)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # print(self.userinfo[0])
        # 发送加入房间消息
        message = {
            "_id": '1',
            "nickname": self.userinfo[0], #nickname
            "headimg": self.userinfo[1],
            "textContent": "{0} 已加入聊天室...".format(self.userinfo[0]),
            "sendTime": time.ctime()
        }
        # print(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message  # 把发送的信息放到event['message']字段里面 ,返回所有信息，数组形式
            }
        )


    async def disconnect(self, close_code):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.session = self.scope["session"]
        self.userinfo = await get_user(self.session)

        await  sub_room(self.room_name,self.session)
        # 退出聊天室向组内所有人广播

        message = {
            "_id": '0',
            "nickname": self.userinfo[0], #nickname
            "headimg": self.userinfo[1],
            "textContent": "{0} 已退出聊天室...".format(self.userinfo[0]),
            "sendTime": time.ctime()
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message  # 把发送的信息放到event['message']字段里面
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # user  = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
        #    'user': 'user',
            'message': message
        }))
