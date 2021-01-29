from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
# from dwebsocket.decorators import accept_websocket
# from dwebsocket.websocket import WebSocket

from authorization.models import Users


class ChatIndexView(View):
    '''获取房间号'''
    def get(self, request):
        try:
            mp = request.GET.get('mp_id')
            query_data = Users.objects.get(id=mp)
            data_list = []
            json_dict = {}
            json_dict['chat_room'] = query_data.chat_room
            data_list.append(json_dict)
            return JsonResponse({"ASGI_CODE": '200', 'ASGI_DATA': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ChatRoomView(View):
    '''消息推送'''
    def get(self, request):
        try:
            open_id = request.GET.get('open_id')
            user_name = request.GET.get('user_name')
            mobile = request.GET.get('mobile')
            content = request.GET.get('content')
            time = request.GET.get('time')
            send = kehuliuyantongzhi(open_id, user_name, mobile, content, time)
            return JsonResponse({"statue": 'success', 'data': send}, safe=False)
        except Exception as e:
            return JsonResponse({"statue": 'false', 'msg': e}, safe=False)
            
