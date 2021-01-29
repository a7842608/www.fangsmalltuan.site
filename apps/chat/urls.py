from django.urls import re_path
from . import views

urlpatterns = [
    # 获取房间号
    re_path(r'room', views.ChatIndexView.as_view()),
    # 传入房间号进入房间
    re_path(r'^xxts/$', views.ChatRoomView.as_view()),
]

