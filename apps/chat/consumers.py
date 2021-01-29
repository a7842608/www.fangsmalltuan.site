from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


class AsyncConsumer(AsyncWebsocketConsumer):

    chats = dict()

    async def connect(self):  # 连接时触发

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name  # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。
        # 将新的连接加入到群组
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        try:
            AsyncConsumer.chats[self.room_name].add(self)
        except:
            AsyncConsumer.chats[self.room_name] = set([self])
        print('长度', len(AsyncConsumer.chats[self.room_name]))
        await self.accept()

    async def disconnect(self, close_code):  # 断开时触发
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        AsyncConsumer.chats[self.room_name].remove(self)
        print('关闭后', len(AsyncConsumer.chats[self.room_name]))

    # 接收消息
    async def receive(self, text_data):
        # print(text_data)
        text_data_json = {'message': text_data}
        message = text_data_json['message']
        message_list = message.split('; ')
        data = [i for i in message_list]

        to_user = data[1]
        print(to_user)

        length = len(AsyncConsumer.chats[self.room_name])
        print(length, '链接数')
        if length == 2:
            print(self.room_group_name, '走到2')
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat.message', # 发送类型: chat.为双通道
                 'connections': length, # 当前链接数
                 'user_room_number': data[0], # 自己的组号
                 'mper_room_number': data[1], # 被接收者的组号
                 'user_header_image': data[2], # 自己的头像
                 # 'mper_header_image': data[3], # 被接收者的头像
                 'message': data[3], # 消息
                 'group': self.room_name # 组名
                 }
            )

        else:
            print(to_user, '走到1')
            await self.channel_layer.group_send(
                'chat_%s' % to_user,
                {
                    "type": "push.message", # 发送类型: push.为单通道
                    'connections': length, # 当前链接数
                    'user_room_number': data[0], # 自己的组号
                    'mper_room_number': data[1], # 被接收者的组号
                    'user_header_image': data[2], # 自己的头像
                    # 'mper_header_image': data[3], # 被接收者的头像
                    'message': data[3], # 消息
                    'group': self.room_name # 组名
                }
            )

    # 从聊天组中接收消息
    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'connections': event['connections'],
            'user_room_number': event['user_room_number'],
            'mper_room_number': event['mper_room_number'],
            'user_header_image': event['user_header_image'],
            # 'mper_header_image': event['mper_header_image'],
            'message': event['message'],
            'group': event['group'],
        }))

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            'type': 'push.message',
            'connections': event['connections'],
            'user_room_number': event['user_room_number'],
            'mper_room_number': event['mper_room_number'],
            'user_header_image': event['user_header_image'],
            # 'mper_header_image': event['mper_header_image'],
            'message': event['message'],
            'group': event['group'],
        }))


# 需要被调用的函数
from channels.layers import get_channel_layer


def push(username, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username,
        {
            "type": "push.message",
            "event": event
        }
    )
