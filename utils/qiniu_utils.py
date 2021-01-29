import threading
import qiniu


class QiniuUtils:
    _instance_lock = threading.Lock()

    def __init__(self, access_key, secret_key):
        self.secret_key = secret_key
        self.access_key = access_key
        self.auth = qiniu.Auth(self.access_key, self.secret_key)
        self.bucket = qiniu.BucketManager(self.auth)
        self.cdn = qiniu.CdnManager(self.auth)

    def __new__(cls, *args, **kwargs):
        if not hasattr(QiniuUtils, '_instance'):
            with QiniuUtils._instance_lock:
                if not hasattr(QiniuUtils, '_instance'):
                    QiniuUtils._instance = object.__new__(cls)
        return QiniuUtils._instance

    def upload(self, bucket_name, key, file_data):
        """
        上传图片到七牛云
        :param bucket_name: 空间名
        :param key: 文件名
        :param file_data: 二进制数据
        :return:
        """
        up_token = self.auth.upload_token(bucket_name, key, 3600)
        return qiniu.put_data(up_token, key, file_data)

    def delete(self, bucket_name, key):
        """
        删除文件
        :param bucket_name:
        :param key:
        :return:
        """
        self.bucket.delete(bucket_name, key)

    def refresh_urls(self, urls):
        self.cdn.refresh_urls(urls)
