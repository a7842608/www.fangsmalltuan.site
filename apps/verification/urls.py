from django.urls import re_path
from . import views

urlpatterns = [
    # 发短信验证码
    # re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),
    re_path(r'^sms_codes/$', views.SmsCodeView.as_view()),

]
