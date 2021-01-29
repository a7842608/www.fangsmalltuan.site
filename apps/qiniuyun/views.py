from qiniu import Auth, put_file, etag
import qiniu.config
from django.http import JsonResponse
from django.views.generic.base import View
from qiniu import put_file

from fang_small_tuan.settings import dev

import io
import uuid
import os

import qiniu
from PIL import Image
from django.conf import settings


class UploadToken(View):
    """七牛云 上传与回调 """
    def post(self, request):
        try:
            uu = request.POST.get('uuid')
            a_id = request.POST.get('user_id')
            img = request.FILES.get('img', None)
            # print(img, type(img))
            access_key = dev.QI_NIU_ACCESS_KEY
            secret_key = dev.QI_NIU_SECRET_KEY
            q = Auth(access_key, secret_key) # 构建鉴权对象
            bucket_name = dev.QI_NIU_BUCKET_NAME # 要上传的空间

            new_uu = str(uuid.uuid4())
            suid = ''.join(new_uu.split('-'))

            _img = img.read()
            size = len(_img) / (1024 * 1024)  # 上传图片的大小 M单位
            # 上传后保存的文件名
            image = Image.open(io.BytesIO(_img))

            name = 'upfile.{0}'.format(image.format)  # 获取图片后缀（图片格式）
            if size > 1:
                # 压缩
                x, y = image.size
                im = image.resize((int(x / 1.73), int(y / 1.73)), Image.ANTIALIAS)  # 等比例压缩 1.73 倍
            else:
                # 不压缩
                im = image
            key = str(a_id) + '_' + str(suid)
            # 要上传文件的本地路径
            # im.save(r'D:\studentstools\pyFiles\project\fang_small_tuan\media' + name)
            im.save(r'.\media' + name)
            # path = r'D:\studentstools\pyFiles\project\fang_small_tuan\media' + name
            path = r'.\media' + name
            token = q.upload_token(bucket_name, key, 3600)
            ret, info = put_file(token, key, path)
            assert ret['key'] == key
            assert ret['hash'] == etag(path)
            url = 'http://tp.kan3721.com/' + ret['key']
            # url = 'http://qhg6mrbju.hn-bkt.clouddn.com/' + ret['key']
            # print(url)

        except Exception as e:
            context = {'CODE':'400', 'ERROR': {e}}
            return JsonResponse(context)

        return JsonResponse({'token': token, 'CODE':'200', 'url': url})
        

class UploadVideoQiniuView(View):
    """七牛云 上传与回调视频 """
    def post(self, request):
        try:
            pt = request.POST.get('path')
            a_id = request.POST.get('user_id')
            bd_id = request.POST.get('only_id')
            # cho = request.POST.get('choice_classfiy')

            access_key = dev.QI_NIU_ACCESS_KEY
            secret_key = dev.QI_NIU_SECRET_KEY
            q = Auth(access_key, secret_key) # 构建鉴权对象
            bucket_name = dev.QI_NIU_BUCKET_NAME # 要上传的空间

            new_uu = str(uuid.uuid4())
            suid = ''.join(new_uu.split('-'))

            path = str(pt)

            key = str(a_id) + '_' + str(suid)
            token = q.upload_token(bucket_name, key, 3600)
            ret, info = put_file(token, key, path)
            assert ret['key'] == key
            assert ret['hash'] == etag(path)
            url = 'http://tp.kan3721.com/' + ret['key']

            os.remove(path)

            return JsonResponse({'token': token, 'CODE': '200', 'url': url})
        except Exception as e:
            context = {'CODE': '400', 'ERROR': {e}}
            return JsonResponse(context)

# def get_FileSize(filePath):
#     filePath = unicode(filePath,'utf8')
#     fsize = os.path.getsize(filePath)
#     fsize = fsize/float(1024*1024)
#     return round(fsize,2)


class UploadVideoView(View):
    '''上传视频'''
    def post(self, request):
        try:
            a_id = request.POST.get('user_id')
            video = request.FILES.getlist('video', None)
            # name = request.POST.get('video_name')
            
            new_uu = str(uuid.uuid4())
            suid = ''.join(new_uu.split('-'))
            
            path_name = str(a_id) + suid
            
            # /www/wwwroot/www.fangsmalltuan.site/media  r'.\media'
            online_path = r'.\media\{}.mp4'.format(path_name)
            # online_path = r'D:\studentstools\pyFiles\project\fang_small_tuan\media\{}.mp4'.format(path_name)

            for f in video:
                file = open(online_path, 'wb+')
                for chunk in f.chunks():
                    file.write(chunk)
                file.close()

            return JsonResponse({'CODE': '200', 'path': online_path})
        except Exception as e:
            context = {'CODE': '400', 'ERROR': {e}}
            return JsonResponse(context)
            
