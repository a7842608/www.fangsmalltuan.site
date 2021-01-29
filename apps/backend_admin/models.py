from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html

from utils.fields import QiniuField


class AccountExecutive(models.Model):
    '''管理账户'''
    user_name = models.CharField(max_length=250, unique=True, blank=True, null=True, verbose_name='账号')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='密码')
    RESIDENCE_CHOICES = ((0, '最高权限'), (1, '一级用户'), (2, '二级用户'), (3, '三级用户'), (4, '四级用户'))
    choice_classfiy = models.SmallIntegerField(choices=RESIDENCE_CHOICES, default=0, verbose_name='类型')

    class Meta:
        db_table = 'tb_account_executive'
        verbose_name = '管理账户'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (self.user_name, self.id, self.password, self.choice_classfiy)
