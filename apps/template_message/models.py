from django.db import models


# Create your models here.


class AAA(models.Model):
    '''地区'''
    values = models.TextField(max_length=5000, blank=True, null=True, verbose_name='监听内容')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')  # 这改了

    class Meta:
        db_table = 'tb_AAA'
        verbose_name = '地区'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s' % (self.id, self.values, self.create_time)


class MessageTemplateValue(models.Model):
    '''消息模板'''
    template_id = models.CharField(max_length=255, unique=True, verbose_name='模板id编号')
    template_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='模板名称')
    template_recode = models.CharField(max_length=255, blank=True, null=True, verbose_name='回复内容')
    CHOICE = ((0, '停止使用'), (1, '正在使用'))
    choice_classfiy = models.SmallIntegerField(choices=CHOICE, default=0, verbose_name='是否使用')

    send_message_time = models.TimeField('定时发送', blank=True, null=True)
    # 0全部,1顾问, 2用户
    class_types = models.SmallIntegerField('接收提醒的用户', default=0, blank=True, null=True)
    # 0开启 1关闭
    status = models.SmallIntegerField('状态', default=0, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_message_template_value'
        verbose_name = '消息模板'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (
            self.id, self.template_id, self.template_recode, self.template_name, self.choice_classfiy, self.create_time)
