from django.urls import re_path
from . import views

urlpatterns = [
    # 发起支付请求
    re_path(r'^pay$', views.PayOrderView.as_view()),
    # 回调支付修改数据库金额
    re_path(r'^callback$', views.CallBackView.as_view()),
]