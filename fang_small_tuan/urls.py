
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # index
    path(r'', include('apps.index.urls')),
    # auth
    path('auth/', include('authorization.urls')),
    # 短信验证码
    path(r'', include('apps.verification.urls')),
    # 七牛云
    path(r'', include('apps.qiniuyun.urls')),
    # 微信支付
    path('wx_pay/', include('pay.urls')),
    # 在线聊天
    path('online/', include('chat.urls')),
    # 富文本编辑器
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # admin
    path('background/', include('backend_admin.urls')),
    # 公众号模板消息推送
    path('wx_gzh/', include('template_message.urls')),

]
