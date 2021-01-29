from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from utils.fields import QiniuField
from django.db.models import SET_NULL


class AttentionMiddlePeopleVillage(models.Model):
    '''顾问关注的楼盘'''
    building_id = models.TextField(blank=True, null=True, verbose_name='楼盘id')
    user_id = models.TextField(blank=True, null=True, verbose_name='顾问id')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间') # 此处有改动

    class Meta:
        db_table = 'tb_attention_middle_people_village'
        verbose_name = '顾问关注的楼盘'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s' % (self.building_id, self.id)
        

class AttentionVillage(models.Model):
    '''用户关注的楼盘'''
    building_id = models.TextField(blank=True, null=True, verbose_name='楼盘id')
    user_id = models.TextField(blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tb_attention_village'
        verbose_name = '用户关注的楼盘'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s' % (self.building_id, self.id)


class AttentionMiddlePeople(models.Model):
    '''用户关注的置业顾问'''
    middle_people_id = models.TextField(blank=True, null=True, verbose_name='置业顾问id')
    user_id = models.TextField(blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tb_attention_middle_people'
        verbose_name = '用户关注的置业顾问'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s' % (self.middle_people_id, self.id)


class AttentionAretical(models.Model):
    '''用户关注的文章'''
    aretical_id = models.TextField(blank=True, null=True, verbose_name='文章id')
    user_id = models.TextField(blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tb_attention_aretial'
        verbose_name = '用户关注的文章'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s' % (self.aretical_id, self.id)


class Users(models.Model):
    '''用户'''
    open_id = models.CharField(max_length=32, unique=True, null=True, blank=True, verbose_name='open_id')
    # 需修改成不默认
    user_uuid = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='user_uuid')

    fk_building = models.ForeignKey(AttentionVillage, on_delete=models.CASCADE, blank=True, null=True, verbose_name='关注的楼盘')
    fk_mp = models.ForeignKey(AttentionMiddlePeople, on_delete=models.CASCADE, blank=True, null=True, verbose_name='关注的置业顾问')
    fk_aretical = models.ForeignKey(AttentionAretical, on_delete=models.CASCADE, blank=True, null=True, verbose_name='关注的文章')

    nick_name = models.CharField(max_length=255, verbose_name='昵称')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    header_img = QiniuField(max_length=255, verbose_name='头像')
    personal_introduce = models.CharField(max_length=255, blank=True, null=True, verbose_name='个人介绍')
    adreess = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    really_name = models.CharField(max_length=25, verbose_name='真实姓名')
    ID_card = models.CharField(max_length=18, unique=True, blank=True, null=True, verbose_name='身份证')
    wechat_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='微信号')
    middle_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='顾问id')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    MIDDLE_PEOPLE_CHOICES = ((0, '普通用户'), (1, '置业顾问'))
    if_middle_people = models.SmallIntegerField(choices=MIDDLE_PEOPLE_CHOICES, default=0, verbose_name='是否是置业顾问')
    chat_room = models.CharField(max_length=500, blank=True, null=True, verbose_name='房间号')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.open_id, self.nick_name, self.mobile, self.header_img, self.personal_introduce,self.really_name, self.ID_card, self.wechat_number, self.create_time, self.fk_building_id, self.fk_mp_id, self.fk_aretical_id)

    def head_img(self):
        return format_html('<img src="{}" width="100px"/>',self.header_img)
    head_img.short_description = u'头像'


class MiddleUnionId(models.Model):
    '''unionid中间表'''
    fk = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户')
    small_open_id = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name='小程序openid')
    gong_open_id = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name='公众号openid')
    union_id = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name='联合id')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tb_middle_union_id'
        verbose_name = 'unionid中间表'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s' % (self.fk_id, self.id, self.small_open_id, self.gong_open_id, self.union_id)


class UserLotteryNumber(models.Model):
    '''用户摇号'''
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户')
    build_id = models.ForeignKey('index.BuildingDetial', on_delete=models.CASCADE, blank=True, null=True, verbose_name='楼盘')
    create_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='用户编码')
    really_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='姓名')

    class Meta:
        db_table = 'tb_user_lottery_number'
        verbose_name = '用户摇号'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (self.number, self.id, self.user_id, self.build_id)

    def u_name(self):
        return self.user_id.nick_name
    u_name.short_description = '用户名称'

    def b_name(self):
        return self.build_id.building_name
    b_name.short_description = '楼盘名称'


class UserCodeNumber(models.Model):
    '''用户编码'''
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户')
    build_id = models.ForeignKey('index.BuildingDetial', on_delete=models.CASCADE, blank=True, null=True, verbose_name='楼盘')
    really_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='姓名')
    create_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='用户编码')
    
    class Meta:
        db_table = 'tb_user_code_number'
        verbose_name = '用户编码'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (self.number, self.id, self.user_id, self.build_id)

    def u_name(self):
        return self.user_id.nick_name
    u_name.short_description = '用户名称'

    def b_name(self):
        return self.build_id.building_name
    b_name.short_description = '楼盘名称'


class MiddlePeople(models.Model):
    '''置业顾问'''
    user_fk = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name='用户',)
    building_fk = models.ForeignKey('index.BuildingDetial', on_delete=models.CASCADE, verbose_name='楼盘')
    room_number = models.CharField(max_length=50,blank=True, null=True, verbose_name='聊天房间号')
    nick_name = models.CharField(max_length=255, verbose_name='昵称')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    header_img = QiniuField(max_length=255, blank=True, null=True,verbose_name='头像')
    personal_introduce = models.CharField(max_length=255, blank=True, null=True, verbose_name='个人介绍')
    really_name = models.CharField(max_length=25,blank=True, null=True, verbose_name='真实姓名')
    ID_card = models.CharField(max_length=18, unique=True, blank=True, null=True, verbose_name='身份证')
    wechat_number = models.TextField(blank=True, null=True, verbose_name='微信号')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    rank = models.CharField(max_length=10, blank=True, null=True, verbose_name='级别')
    bussiness_building = models.CharField(max_length=255, blank=True, null=True, verbose_name='主营楼盘')
    browse_count = models.IntegerField(default=0, verbose_name='浏览量')
    live_limit = models.IntegerField(default=0, verbose_name='活跃度')
    click_count = models.IntegerField(default=0, verbose_name=' 点赞数')
    call_mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='通过的电话')
    wechat_talk = models.TextField(blank=True, null=True, verbose_name='微聊')
    exclusive_people = models.CharField(max_length=50, blank=True, null=True, verbose_name='专属客户')
    integral = models.IntegerField(default=0, null=True, blank=True, verbose_name='积分')
    golden_money = models.IntegerField(default=0, null=True, blank=True, verbose_name='金币')
    give_price_history = models.CharField(max_length=100, null=True, blank=True, verbose_name='出价记录')
    invitation_code = models.CharField(max_length=15, blank=True, null=True, unique=True, verbose_name='邀请码')
    two_wei_ma = QiniuField(max_length=5000, null=True,blank=True,  verbose_name='二维码')
    work_pai = QiniuField(max_length=5000, blank=True, null=True, verbose_name='工牌')

    class Meta:
        db_table = 'tb_middle_people'
        verbose_name = '置业顾问'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.nick_name,self.mobile,self.header_img,self.personal_introduce, self.really_name, self.ID_card,self.wechat_number,self.create_time, self.rank, self.browse_count, self.live_limit, self.click_count, self.wechat_talk, self.exclusive_people, self.integral, self.golden_money, self.give_price_history, self.invitation_code, self.two_wei_ma, self.work_pai)

    def u_name(self):
        return self.user_fk.nick_name
    u_name.short_description = '用户名称'

    def b_name(self):
        return self.building_fk.building_name
    b_name.short_description = '楼盘名称'

    def head_img(self):
        return format_html('<img src="{}" width="100px"/>',self.header_img)
    head_img.short_description = u'头像'


class QuestionFeedback(models.Model):
    '''问题反馈'''
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')

    QUESTION_CHOICES = ((0, '程序错误'), (1, '优化建议'), (2, '数据错误/缺失'), (3, '其他'))
    choice_classfiy = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='反馈类型')
    my_create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='问题创建时间')
    my_content = RichTextUploadingField(blank=True, null=True, verbose_name='问题描述内容')
    question_img = QiniuField(max_length=5000, blank=True, null=True, verbose_name='问题图片')
    feedback_phone = models.CharField(max_length=11 ,null=True,blank=True, verbose_name='联系方式')
    img1 = QiniuField(max_length=5000, blank=True, null=True, verbose_name='问题图片')
    
    class Meta:
        db_table = 'tb_question_feedback'
        verbose_name = '问题反馈'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.id, self.user_id, self.choice_classfiy, self.my_create_time, self.my_content, self.feedback_phone, self.question_img)

    def image1(self):
        return format_html('<img src="{}" width="100px"/>',self.question_img)
    image1.short_description = u'问题图片1'

    def image2(self):
        return format_html('<img src="{}" width="100px"/>',self.img1)
    image2.short_description = u'问题图片2'

    def u_name(self):
        return self.user.nick_name
    u_name.short_description = '用户名称'


class MyPhoneCall(models.Model):
    '''我的来电'''
    middle_people = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='所属置业顾问')
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='来电人名称')
    user_id = models.CharField(max_length=30, null=True, blank=True, verbose_name='通过电话的id')
    phone_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='通话创建时间')
    user_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='电话号码')
    create_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='数据创建时间')
    head_img = QiniuField(max_length=255, blank=True, null=True, verbose_name='头像')
    CHANGE_CHOICES = ((0, '已结'), (1, '未接'))
    choice_classfiy = models.SmallIntegerField(choices=CHANGE_CHOICES, default=0, verbose_name='接打类型')

    class Meta:
        db_table = 'tb_my_phone_call'
        verbose_name = '我的来电'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.id, self.name, self.user_id, self.middle_people_id, self.phone_time, self.user_phone, self.create_time, self.head_img, self.choice_classfiy)

    def header_img(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    header_img.short_description = u'头像'

    def u_name(self):
        return self.middle_people.nick_name
    u_name.short_description = '顾问名称'


class ExclusiveCustmer(models.Model):
    '''专属客户'''
    middle_name = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问')
    user_id = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='用户id')
    user_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='普通用户姓名')
    custmer_time = models.DateTimeField(auto_now_add=True, blank=True,null=True, verbose_name='关注时间')
    create_time = models.DateField(auto_now_add=True, blank=True,null=True, verbose_name='数据创建时间')
    head_img = QiniuField(max_length=255, blank=True, null=True, verbose_name='头像')

    class Meta:
        db_table = 'tb_exclusive_custmer'
        verbose_name = '专属客户'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.middle_name_id, self.user_id, self.id, self.user_name, self.custmer_time, self.create_time, self.head_img)

    def header_img(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    header_img.short_description = u'头像'

    def u_name(self):
        return self.middle_name.nick_name
    u_name.short_description = '顾问名称'


class MyWeChat(models.Model):
    '''我的微聊'''
    middle_name = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问')
    user_id = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='用户id')
    user_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='普通用户姓名')
    custmer_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='沟通时间')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')
    head_img = QiniuField(max_length=255, blank=True, null=True, verbose_name='头像')
    where_come_from = models.TextField(blank=True, null=True, verbose_name='来源')
    CHANGE_CHOICES = ((0, '已读'), (1, '未读'))
    choice_classfiy = models.SmallIntegerField(choices=CHANGE_CHOICES, default=0, verbose_name='读取类型')

    class Meta:
        db_table = 'tb_my_we_chat'
        verbose_name = '我的微聊'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.where_come_from, self.middle_name_id, self.user_id, self.id, self.user_name, self.custmer_time, self.create_time, self.head_img, self.choice_classfiy)

    def header_img(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    header_img.short_description = u'头像'

    def u_name(self):
        return self.middle_name.nick_name
    u_name.short_description = '顾问名称'


class GoldenMoney(models.Model):
    '''金币明细表'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问')
    money_count = models.IntegerField(default=0, blank=True, null=True, verbose_name='金币修改数量')
    recharge_time = models.DateField(auto_now=True, blank=True, null=True, verbose_name='修改时间')
    change_beacuse = models.CharField(max_length=255, blank=True, null=True, verbose_name='修改原因')
    create_time = models.DateField(auto_now=True, blank=True, null=True, verbose_name='数据创建时间')
    CHANGE_CHOICES = ((0, '收入'), (1, '支出'))
    choice_classfiy = models.SmallIntegerField(choices=CHANGE_CHOICES, default=0, verbose_name='收支类型')

    class Meta:
        db_table = 'tb_golden_money'
        verbose_name = '金币表'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.fk_id, self.money_count, self.recharge_time, self.id, self.change_beacuse, self.create_time, self.choice_classfiy)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class IntegralSubsidiary(models.Model):
    '''积分明细表'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问')
    score = models.IntegerField(default=0, blank=True, null=True, verbose_name='积分修改数量数')
    score_create_time = models.DateField(auto_now=True, blank=True, null=True, verbose_name='修改时间')
    change_beacuse = models.CharField(max_length=255, blank=True, null=True, verbose_name='修改原因')
    create_time = models.DateField(auto_now=True, blank=True, null=True, verbose_name='数据创建时间')
    CHANGE_CHOICES = ((0, '增加'), (1, '减少'))
    choice_classfiy = models.SmallIntegerField(choices=CHANGE_CHOICES, default=0, verbose_name='积分加减类型')

    class Meta:
        db_table = 'tb_integral_subsidiary'
        verbose_name = '积分表'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.fk_id, self.score, self.score_create_time, self.id, self.change_beacuse, self.create_time,self.choice_classfiy)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class GaoIndexPKMoney(models.Model):
    '''首页广告竞价'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问名称')
    building_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='准备上首页的id')
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name='出价金额')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='数据创建时间')

    class Meta:
        db_table = 'tb_gao_index_pk_money'
        verbose_name = '首页广告竞价'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s' % (self.fk_id, self.id, self.building_id, self.price, self.create_time)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class GaoBuildingDetialPKMoney(models.Model):
    '''楼盘详情页竞价'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问名称')
    building_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='准备上楼盘详情页的id')
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name='出价金额')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='数据创建时间')

    class Meta:
        db_table = 'tb_gao_building_detial_pk_money'
        verbose_name = '楼盘详情页竞价'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s' % (self.fk_id, self.id, self.building_id, self.price, self.create_time)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class WhoLookMiddelPeople(models.Model):
    '''顾问访客'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问名称')
    user_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')

    class Meta:
        db_table = 'tb_who_look_middle_people'
        verbose_name = '顾问访客'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (self.fk_id, self.id, self.user_id, self.create_time)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class WhoZanMiddelPeople(models.Model):
    '''用户点赞了顾问'''
    fk = models.ForeignKey(MiddlePeople, on_delete=SET_NULL, blank=True, null=True, verbose_name='置业顾问名称')
    user_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户id')
    middle_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='顾问id')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')

    class Meta:
        db_table = 'tb_who_zan_middle_people'
        verbose_name = '顾问点赞记录'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (self.fk_id, self.id, self.user_id, self.create_time)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class MiddlePeopleHistoryMessageRecord(models.Model):
    '''顾问历史消息记录'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='置业顾问名称')
    user_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户id')
    middle_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='顾问id')
    content = models.TextField(blank=True, null=True, verbose_name='说话记录')
    create_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='数据创建时间')
    room = models.CharField(max_length=255, blank=True, null=True, verbose_name='当时的房间号')

    class Meta:
        db_table = 'tb_middle_people_history_message_record'
        verbose_name = '顾问聊天记录'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.fk_id, self.id, self.user_id, self.create_time, self.middle_id, self.content)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'


class UserHistoryMessageRecord(models.Model):
    '''用户历史消息记录'''
    fk = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    user_bei_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='被聊人id')
    content = models.TextField(blank=True, null=True, verbose_name='说话记录')
    create_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='数据创建时间')
    room = models.CharField(max_length=255, blank=True, null=True, verbose_name='房间号')
    header_image = QiniuField(max_length=255, blank=True, null=True,  verbose_name='用户头像')
    # CHANGE_CHOICES = ((0, '增加'), (1, '减少'))
    # choice_classfiy = models.SmallIntegerField(choices=CHANGE_CHOICES, default=0, verbose_name='积分加减类型')

    class Meta:
        db_table = 'tb_user_history_message_record'
        verbose_name = '用户聊天记录'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s' % (self.fk_id, self.id, self.user_bei_id, self.create_time, self.content)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '用户名称'


class ReallyNameMiddlePeopleShare(models.Model):
    '''来路分析'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, verbose_name='所属顾问')
    user_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户id')
    middle_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='顾问id')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='来源')

    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')

    class Meta:
        db_table = 'tb_really_name_middle_people_share'
        verbose_name = '获客神器'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.fk_id, self.id, self.user_id, self.create_time, self.middle_id, self.name)

    def u_name(self):
        return self.fk.nick_name
    u_name.short_description = '顾问名称'
    
    
class UserReport(models.Model):
    '''举报表'''
    fk = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')
    classfiy1 = models.CharField(max_length=50, blank=True, null=True, verbose_name='举报类型1')
    classfiy2 = models.CharField(max_length=50, blank=True, null=True, verbose_name='举报类型2')
    upload_img1 = QiniuField(max_length=500, blank=True, null=True, verbose_name='上传问题图片1')
    upload_img2 = QiniuField(max_length=500, blank=True, null=True, verbose_name='上传问题图片2')
    upload_img3 = QiniuField(max_length=500, blank=True, null=True, verbose_name='上传问题图片3')
    upload_img4 = QiniuField(max_length=500, blank=True, null=True, verbose_name='上传问题图片4')
    upload_img5 = QiniuField(max_length=500, blank=True, null=True, verbose_name='上传问题图片5')
    upload_img6 = QiniuField(max_length=500, blank=True, null=True, verbose_name='上传问题图片6')
    content = models.CharField(max_length=9999, blank=True, null=True, verbose_name='问题描述')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    user_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户名')
    bad_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='被举报人id')

    class Meta:
        db_table = 'tb_user_report'
        verbose_name = '举报表'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.id, self.fk_id, self.classfiy1, self.classfiy2, self.content, self.mobile)

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>', self.upload_img)
    image_data.short_description = u'问题图片'


class UserLoginRecord(models.Model):
    '''登陆记录'''
    fk = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now=True, verbose_name='数据创建时间')
    user_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户名')
    header_img = QiniuField(max_length=500, blank=True, null=True, verbose_name='头像')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_user_login_record'
        verbose_name = '登陆记录表'
        verbose_name_plural = verbose_name
        managed = True
        
        
class UserLoginBuildingRecord(models.Model):
    '''用户访问楼盘记录'''
    fk = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now=True, verbose_name='数据创建时间')
    user_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户名')
    building_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='楼盘id')
    header_img = QiniuField(max_length=500, blank=True, null=True, verbose_name='头像')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_user_login_building_record'
        verbose_name = '用户访问楼盘记录'
        verbose_name_plural = verbose_name
        managed = True
        

class UserSealStatus(models.Model):
    '''用户封禁状态'''
    open_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户open_id')
    create_time = models.DateTimeField(auto_now=True, verbose_name='数据创建时间')
    statue = models.BooleanField(default=False, verbose_name='是否封号')
    QUESTION_CHOICES = ((0, '无'), (1, '7天'), (2, '30天'), (3, '永久'))
    choice_classfiy = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='封印类型')
    if_talk = models.BooleanField(default=False, verbose_name='是否禁言')
    
    class Meta:
        db_table = 'tb_user_seal_status'
        verbose_name = '用户封禁状态'
        verbose_name_plural = verbose_name
        managed = True
        
        
class SensitiveWord(models.Model):
    '''敏感词'''
    create_time = models.DateField(auto_now=True, verbose_name='数据创建时间')
    word = models.CharField(max_length=255, blank=True, null=True, verbose_name='词')
    QUESTION_CHOICES = ((0, '无'), (1, '顾问'), (2, '用户'), (3, '全局'))
    choice_classfiy = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='作用域')
    
    class Meta:
        db_table = 'tb_sensitive_word'
        verbose_name = '敏感词'
        verbose_name_plural = verbose_name
        managed = True


class MaxConnectionAndMaxPeopleAndMaxCountView(models.Model):
    '''聊天人数上限, 聊天次数, 限制时间'''
    create_time = models.DateField(auto_now=True, verbose_name='数据创建时间')
    chat_second = models.CharField(max_length=255, blank=True, null=True,  verbose_name='聊天限制时间/秒数')
    chat_people = models.CharField(max_length=255, blank=True, null=True, verbose_name='最大人数')
    chat_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='最大聊天次数')
    ip_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='最大请求次数')
    
    class Meta:
        db_table = 'tb_chat_connection'
        verbose_name = '聊天人数上限, 聊天次数, 限制时间'
        verbose_name_plural = verbose_name
        managed = True
        
        
class MessageChatListView(models.Model):
    '''即时通讯聊天列表'''
    create_time = models.DateTimeField(auto_now=True, verbose_name='数据创建时间')
    fk = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id')
    header_image = QiniuField(max_length=255, blank=True, null=True,  verbose_name='用户头像')
    message = models.CharField(max_length=500, blank=True, null=True, verbose_name='消息记录')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户名称')
    pid = models.CharField(max_length=255, blank=True, null=True, verbose_name='列表中显示的顾问id')
    ur_room = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户的房间号')
    mp_room = models.CharField(max_length=255, blank=True, null=True, verbose_name='顾问的房间号')

    class Meta:
        db_table = 'tb_message_chat_list'
        verbose_name = '即时通讯聊天列表'
        verbose_name_plural = verbose_name
        managed = True


class Token(models.Model):
    create_time = models.DateTimeField(auto_now=True, verbose_name='数据创建时间')
    token = models.CharField(max_length=255, blank=True, null=True, verbose_name='token')

    class Meta:
        db_table = 'tb_token'
        verbose_name = 'token'
        verbose_name_plural = verbose_name
        managed = True


class UserEveryDayPermetionStatue(models.Model):
    '''用户每日任务状态栏'''
    fk = models.ForeignKey(MiddlePeople, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id')
    QUESTION_CHOICES = ((0, '否'), (1, '是'))
    q_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='今日是否签到')
    q_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='连续签到天数')
    g_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否授权关注公众号')
    fn_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否分享给新用户')
    fn_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='分享给新用户次数')
    fo_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否分享给老用户')
    fo_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='分享给老用户次数')
    zf_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否转发朋友圈')
    zf_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='转发朋友圈次数')
    fxt_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否发布分享唐')
    fxt_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='发布分享唐次数')
    tgxx_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否提供重要信息')
    tgxx_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='提供重要信息次数')
    yqrz_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否邀请置业顾问入驻')
    yqrz_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='邀请置业顾问入驻次数')
    sclp_choice = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='是否上传楼盘信息')
    sclp_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='上传楼盘信息次数')
    create_time = models.DateTimeField(auto_now=True, verbose_name='数据创建时间')


    class Meta:
        db_table = 'tb_user_everyday_permetion_statue'
        verbose_name = '用户每日任务状态栏'
        verbose_name_plural = verbose_name
        managed = True

