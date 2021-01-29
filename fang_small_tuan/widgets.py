from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template import loader
from django.utils.safestring import mark_safe

from fang_small_tuan.settings import dev
from utils.qiniu_utils import QiniuUtils


class QiniuWidgets(forms.FileInput):
    # template_name = 'admin/qiniu_input.html'

    def __init__(self, attrs=None, app=None, table=None, unique_list=None):
        """
        :param attrs:
        :param app: app
        :param table: 数据模型
        :param unique_list: 唯一标识列表，除了id
        """
        super(QiniuWidgets, self).__init__(attrs)
        self.unique = unique_list
        if dev.DEBUG:
            env = 'dev'
        else:
            env = 'pro'
        self.filename_prefix = '{}/{}/{}/'.format(env, app, table)

    def format_value(self, value):
        return value

    def value_from_datadict(self, data, files, name):
        file = files.get(name)  # type:InMemoryUploadedFile
        file_data = b''.join(chunk for chunk in file.chunks()) # 取出二进制数据
        file_type = file.name.split('.')[-1] # 得到文件的后缀
        unique_filename = '_'.join(list(map(lambda x: data.get(x), self.unique)))
        file_name = self.filename_prefix + '{}_{}.{}'.format(name, unique_filename, file_type) # 构造文件的唯一文件名
        q = QiniuUtils(dev.QI_NIU_ACCESS_KEY, dev.QI_NIU_SECRET_KEY) # 七牛上传实例
        q.delete(dev.QI_NIU_BUCKET_NAME, file_name) # 删除已经存在的
        q.upload(dev.QI_NIU_BUCKET_NAME, file_name, file_data) # 上传新的
        # http = 'https://' if dev.QI_NIU_SSL else 'http://'
        # url = http + dev.QI_NIU_ACCESS_DOMAIN + '/' + file_name # 拼接最终的url
        url = 'http://qhg6mrbju.hn-bkt.clouddn.com/' + file_name # 拼接最终的url
        return url

    # def render(self, name, value, attrs=None, renderer=None):
    #     context = self.get_context(name, value, attrs)
    #     template = loader.get_template(self.template_name).render(context)
    #     return mark_safe(template)
