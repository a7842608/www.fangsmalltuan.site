from django.urls import re_path
from . import views

urlpatterns = [
    # 上传与回调
    re_path('upload/', views.UploadToken.as_view(), name='upload_token'),
    
    # 上传并返回path地址
    re_path('upload_video/', views.UploadVideoView.as_view()),
    # 七牛云上传视频接口
    re_path('upload_video_qiniu/', views.UploadVideoQiniuView.as_view()),
    
]