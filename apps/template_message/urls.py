from django.urls import re_path
from . import views

urlpatterns = [
    # access_token
    # re_path(r'^access_token$', views.AccessTokenView.as_view()),
    # 获取unionid 并入库
    re_path(r'^encryptedData$', views.RequestEncodeEnterDatabaseView.as_view()),
    # 发送模板消息
    re_path(r'^stm$', views.SendTemplateMessageView.as_view()),
    # 验证开发者模式
    re_path(r'^yzkfzms$', views.ReciveCheckGZHView.as_view()),
    # token签发与验证
    re_path(r'^tttksxbxyxl$', views.TokenGiveQianView.as_view()),
]