from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import format_html
from ckeditor_uploader.fields import RichTextUploadingField
from utils.fields import QiniuField


class LandDistrict(models.Model):
    '''地区'''
    name = models.CharField(max_length=10, blank=True, null=True, verbose_name='区名')
    # longitude = models.CharField(max_length=255, verbose_name='经度')
    key_name = models.CharField(max_length=255, verbose_name='经纬度')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间') # 这改了
    
    class Meta:
        db_table = 'tb_land_district'
        verbose_name = '地区'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s' % (self.id,self.name, self.key_name)


class Subway(models.Model):
    '''地铁'''
    name = models.CharField(max_length=10, blank=True, null=True, verbose_name='地铁线路名称')
    key_name = models.CharField(max_length=10, verbose_name='类别键名')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间') # 这改了
    
    class Meta:
        db_table = 'tb_subway'
        verbose_name = '地铁'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s' % (self.id, self.name, self.key_name)


class SubwayStation(models.Model):
    '''地铁站'''
    subway = models.ForeignKey(Subway, on_delete=models.CASCADE, verbose_name='地铁')
    name = models.CharField(max_length=10, blank=True, null=True, verbose_name='地铁站名称')
    key_name = models.CharField(max_length=10, verbose_name='类别键名')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间') # 这改了

    class Meta:
        db_table = 'tb_subway_station'
        verbose_name = '地铁站'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s' % (self.id, self.name, self.key_name)

    def suby_name(self):
        return self.subway.name
    def suby_id(self):
        return self.subway.id
    suby_name.short_description = '地铁站'
    suby_id.short_description = '地铁站id'


class BuildingClassfiy(models.Model):
    """楼盘性质类型(限购/闭眼/地铁/倒挂/线上售楼部/改善房/无需摇号/优质)"""
    name = models.CharField(max_length=50, verbose_name='名称')
    key_name = models.CharField(max_length=50, verbose_name='类别键名')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间') # 这改了
    
    class Meta:
        db_table = 'tb_budling_classfiy'
        verbose_name = '楼盘其他类型'
        managed = True
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s %s' % (self.id, self.name, self.key_name)


class BuildingDetial(models.Model):
    '''楼盘详情'''
    '''主表'''
    '''类型'''
    land = models.ForeignKey(LandDistrict, on_delete=models.CASCADE, null=True, blank=True, verbose_name='地区')
    train = models.ForeignKey(SubwayStation, on_delete=models.CASCADE, null=True, blank=True, verbose_name='地铁站')
    budling_other = models.ForeignKey(BuildingClassfiy, on_delete=models.CASCADE, null=True, blank=True, verbose_name='楼盘其他类型')

    '''销售信息'''
    building_name = models.CharField(max_length=20, verbose_name='楼房名称')
    total_price = models.CharField(max_length=10, blank=True, null=True, verbose_name='参考总价')
    unit_price = models.CharField(max_length=100, blank=True, null=True, verbose_name='参考单价')
    house_section = models.CharField(max_length=20, blank=True, null=True, verbose_name='户型')
    sale_stage = models.CharField(max_length=20, blank=True, null=True, verbose_name='销售阶段')
    sale_stage_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='销售阶段截止日期')
    sale_building_location = models.CharField(max_length=50,blank=True, null=True,  verbose_name='售楼地址')
    premises_location = models.CharField(max_length=50,blank=True, null=True,  verbose_name='楼盘地址')
    delivery_time = models.CharField(max_length=25, blank=True, null=True, verbose_name='交房时间')
    '''经纬度'''
    longitude = models.CharField(max_length=255, blank=True, null=True, verbose_name='经度')
    latitude = models.CharField(max_length=255, blank=True, null=True, verbose_name='纬度')
    '''基本信息'''
    building_nickname = models.CharField(max_length=20, blank=True, null=True, verbose_name='楼盘别名')
    building_classfiy = models.CharField(max_length=20, blank=True, null=True, verbose_name='楼盘类型')
    equity_year = models.CharField(max_length=20, blank=True, null=True, verbose_name='产权年限')
    green_rate = models.CharField(max_length=10, blank=True, null=True, verbose_name='绿化率')
    volume_rate = models.CharField(max_length=10, blank=True, null=True, verbose_name='容积率')
    stall_message = models.CharField(max_length=20, blank=True, null=True, verbose_name='车位信息')
    cube_count = models.CharField(max_length=20, blank=True, null=True, verbose_name='楼栋数')
    all_house_count = models.CharField(max_length=20, blank=True, null=True, verbose_name='总户数')
    floor_space = models.CharField(max_length=20, blank=True, null=True, verbose_name='占地面积')
    covered_area = models.CharField(max_length=20, blank=True, null=True, verbose_name='建筑面积')
    covered_classfiy = models.CharField(max_length=20, blank=True, null=True, verbose_name='建筑类型')
    covered_tier = models.CharField(max_length=20, blank=True, null=True, verbose_name='建筑楼层')
    company = models.CharField(max_length=50, blank=True, null=True, verbose_name='物业公司')
    company_money = models.CharField(max_length=50, blank=True, null=True, verbose_name='物业费')
    upstart = models.CharField(max_length=50, blank=True, null=True, verbose_name='开发商')
    tier_condition = models.CharField(max_length=100, blank=True, null=True, verbose_name='楼层状况')
    '''周边配套'''
    train_traffic = models.CharField(max_length=255, blank=True, null=True, verbose_name='地铁交通')
    bus_site = models.CharField(max_length=255, blank=True, null=True, verbose_name='公交站点')
    school = models.CharField(max_length=255, blank=True, null=True, verbose_name='学校')
    bank = models.CharField(max_length=255, blank=True, null=True, verbose_name='银行')
    catering = models.CharField(max_length=100, blank=True, null=True, verbose_name='餐饮')
    hospital = models.CharField(max_length=255, blank=True, null=True, verbose_name='医院')
    shopping = models.CharField(max_length=255, blank=True, null=True, verbose_name='购物中心')
    park = models.CharField(max_length=255, blank=True, null=True, verbose_name='公园')
    other_mating = models.TextField(blank=True, null=True, verbose_name='其他配套')
    '''简介'''
    building_intro = RichTextUploadingField(blank=True, null=True, verbose_name='楼盘简介')
    '''广告与关注'''
    AD_INDEX_CHOICES = ((0, 'yes'),(1, 'no'))
    AD_BUILDING_CHOICES = ((0, 'yes'),(1, 'no'))
    LUN_BO_CHOICES = ((0, 'yes'),(1, 'no'))
    if_index_advertising = models.SmallIntegerField(choices=AD_INDEX_CHOICES, default=0, verbose_name='是否在首页广告')
    if_lunbo_choice = models.SmallIntegerField(choices=LUN_BO_CHOICES, default=0, verbose_name='是否轮播图')
    if_building_detail_advertising = models.SmallIntegerField(choices=AD_BUILDING_CHOICES, default=0, verbose_name='是否在楼盘广告')
    attention_degree = models.IntegerField(default=0, blank=True, null=True, verbose_name='浏览量')
    comment_count = models.IntegerField(default=0, blank=True, null=True, verbose_name='评论量')
    '''开盘信息'''
    open_house_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='开盘栋数')
    open_price = models.CharField(blank=True, null=True, max_length=50, verbose_name='开盘价格')
    decorate_situation = models.CharField(max_length=20, blank=True, null=True, verbose_name='装修情况')
    open_house_section = models.CharField(max_length=20, blank=True, null=True, verbose_name='开盘户型区间')
    open_house_count = models.CharField(max_length=20,blank=True, null=True,  verbose_name='开盘房源套数')
    registration_way = models.CharField(max_length=20, blank=True, null=True, verbose_name='报名方式')
    cool_captial_request = models.CharField(max_length=20, blank=True, null=True, verbose_name='冻资要求')
    '''楼盘房源类型'''
    house_count = models.CharField(max_length=50,blank=True, null=True,  verbose_name='房源套数') #??切换楼栋?
    people_count = models.CharField(max_length=30,blank=True, null=True,  verbose_name='报名人数')
    win_probability = models.CharField(max_length=30,blank=True, null=True,  verbose_name='摇中概率')

    will_sale_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='预售证号')
    give_number_time = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name='发证时间')
    lottery_count = models.CharField(max_length=50, null=True, blank=True, verbose_name='摇号批次')

    building_create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='开盘时间')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')
    union_building_test_id = models.IntegerField(blank=True, null=True, verbose_name='楼盘联合id')

    class Meta:
        db_table = 'tb_building_detial'
        verbose_name = '楼盘详情'
        managed = True
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.id,self.will_sale_number,self.give_number_time,self.lottery_count, self.building_create_time, self.win_probability, self.people_count, self.house_count, self.cool_captial_request, self.registration_way, self.open_house_count, self.open_house_section, self.decorate_situation, self.open_house_number, self.comment_count, self.attention_degree, self.if_index_advertising, self.if_building_detail_advertising, self.building_intro, self.other_mating, self.park, self.shopping, self.catering, self.hospital, self.bank, self.bus_site, self.train_traffic, self.tier_condition, self.upstart, self.company, self.covered_tier, self.covered_classfiy, self.covered_area, self.floor_space, self.all_house_count, self.cube_count, self.stall_message, self.volume_rate, self.green_rate, self.equity_year, self.building_classfiy, self.building_nickname, self.latitude, self.longitude, self.delivery_time, self.premises_location, self.sale_building_location, self.sale_stage, self.house_section, self.unit_price, self.total_price, self.building_name, self.budling_other.name, self.train.name, self.land.name, self.if_lunbo_choice, self.company_money)


class HistoryLottery(models.Model):
    '''历史摇号信息(新旧)'''
    detial = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘id')
    lottery_time = models.CharField(max_length=50, blank=True, null=True, verbose_name='摇号时间')
    one_price = models.IntegerField(default=0, blank=True, null=True, verbose_name='参考单价')
    all_price = models.IntegerField(default=0, blank=True, null=True, verbose_name='参考总价')
    decorate_situation = models.CharField(max_length=20, blank=True, null=True, verbose_name='装修情况')
    house = models.CharField(max_length=20, blank=True, null=True, verbose_name='主力户型')
    cool_captial_request = models.CharField(max_length=20, blank=True, null=True, verbose_name='冻资要求')
    house_count = models.CharField(max_length=50, verbose_name='房源套数')  # ??切换楼栋?
    people_count = models.CharField(max_length=30, verbose_name='报名人数')
    win_probability = models.CharField(max_length=30, verbose_name='摇中概率')

    class Meta:
        db_table = 'tb_history_lottery'
        verbose_name = '历史摇号信息'
        managed = True
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s' %(self.id, self.detial.id, self.lottery_time, self.one_price, self.all_price, self.decorate_situation, self.house, self.cool_captial_request, self.people_count, self.win_probability)

    def name(self):
        return self.detial.building_name
    name.short_description = '楼盘名称'


class OneHouseOnePrice(models.Model):
    '''一房一价'''
    building_detial = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, blank=True, null=True, verbose_name='楼盘详情')
    house_dong = models.CharField(max_length=10, blank=True, null=True, verbose_name='楼栋')    # 1
    house_yuan = models.CharField(max_length=10, blank=True, null=True, verbose_name='单元')    # 1, 1
    house_ceng = models.CharField(max_length=10, blank=True, null=True, verbose_name='楼层')    # 1, 1
    door_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='门牌号')  # 1, 1, 1, 101
    create_area = models.CharField(max_length=255, blank=True, null=True, verbose_name='建面面积')
    in_area = models.CharField(max_length=255, blank=True, null=True, verbose_name='套内面积')
    gave_house = models.CharField(max_length=255, blank=True, null=True, verbose_name='得房率')
    one_price = models.CharField(max_length=255, blank=True, null=True, verbose_name='单价')
    all_price = models.CharField(max_length=255, blank=True, null=True, verbose_name='总价')
    will_sale_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='预售证号')
    public_date = models.CharField(max_length=255, blank=True, null=True, verbose_name='公示日期')
    give_date = models.CharField(max_length=255, blank=True, null=True, verbose_name='核发日期')
    build_company = models.CharField(max_length=255, blank=True, null=True, verbose_name='开发商')
    lottery_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='地块编号') # 杭钱塘出处
    create_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='数据创建时间')
    all_tao_count = models.CharField(max_length=255, blank=True, null=True, verbose_name='总套数')
    house_use = models.CharField(max_length=255, blank=True, null=True, verbose_name='使用类型')
    
    class Meta:
        db_table = 'tb_one_house_one_price'
        verbose_name = '一房一价'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s' % (self.id)


class BuildingStatueTimeSale(models.Model):
    """楼盘销售时间(预售/摇号/公示/摇号/补交资料)"""
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘详情')
    history = models.ForeignKey(HistoryLottery, on_delete=models.CASCADE, blank=True,null=True, verbose_name='历史摇号id')
    will_sale_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='预售时间')
    register_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='登记时间')
    commit_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='补交资料时间')
    want_told_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='意向公示时间')
    lottery_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='摇号时间')
    choice_house_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='选房时间')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间') # 这改了

    class Meta:
        db_table = 'tb_budling_statue_time_sale'
        verbose_name = '楼盘销售时间'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.id, self.fk.building_name, self.will_sale_time, self.register_time, self.commit_time, self.want_told_time, self.lottery_time, self.choice_house_time)

    def b_name(self):
        return self.fk.building_name

    b_name.short_description = '楼盘名称'


class UnionLotteryResult(models.Model):
    '''摇号结果/意向登记联合表'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, null=True, blank=True, verbose_name='楼盘')
    pid = models.CharField(max_length=500, blank=True, null=True, verbose_name='PID')
    building_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='楼盘名称')
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_union_lottery_result'
        verbose_name = '购房登记号顺序表(摇号结果)'
        managed = True
        verbose_name_plural = verbose_name


class LotteryResult(models.Model):
    '''购房登记号顺序表(摇号结果)'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, null=True, blank=True, verbose_name='楼盘')
    pid = models.CharField(max_length=500, blank=True, null=True, verbose_name='PID')
    serial_number = models.CharField(max_length=255,null=True, blank=True, verbose_name='序号')
    buy_house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='购房登记号')
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_lottery_result'
        verbose_name = '购房登记号顺序表(摇号结果)'
        managed = True
        verbose_name_plural = verbose_name


class ToldPurpose(models.Model):
    '''意向登记表'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, blank=True, null=True, verbose_name='楼盘')
    pid = models.CharField(max_length=500, blank=True, null=True, verbose_name='PID')
    building_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='楼盘名称')
    buy_house_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='购房登记号')
    lottery_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='购房人姓名')
    ID_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='购房人身份证号')
    house_classfiy = models.CharField(max_length=255, blank=True, null=True, verbose_name='家庭类型')
    find_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='查档编号')
    other_lottery_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='家庭成员姓名')
    other_ID_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='其他人身份证号')
    CHECK_CHOICES = ((0, 'no'), (1, 'yes'))
    audit_status = models.SmallIntegerField(choices=CHECK_CHOICES, default=0, null=True, blank=True, verbose_name='审核状态')
    WIN_CHOICES = ((0, 'no'), (1, 'yes'))
    if_win_lottery = models.SmallIntegerField(choices=WIN_CHOICES, default=0,  null=True, blank=True,verbose_name='是否中签')
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_told_purpose'
        verbose_name = '意向登记'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.fk_id, self.building_name, self.buy_house_number, self.lottery_name, self.ID_number, self.house_classfiy, self.find_number, self.other_lottery_name, self.other_ID_number, self.audit_status, self.if_win_lottery)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '楼盘名称'


class IssueBuildingDynamicMessage(models.Model):
    '''(发表)楼盘动态信息(房小团官宣)'''
    building_detial = models.ForeignKey(BuildingDetial, on_delete=models.PROTECT,null=True, blank=True, verbose_name='楼盘')
    title = models.CharField(max_length=255,null=True, blank=True, verbose_name='标题')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    message_create_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    author = models.CharField(max_length=50,null=True, blank=True, verbose_name='作者')
    author_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='作者id')
    RESIDENCE_CHOICES = ((0, '无'), (1, '楼盘动态'), (2, '预售证'), (3, '开盘'), (4, '交房'))
    choice_classfiy = models.SmallIntegerField(choices=RESIDENCE_CHOICES, default=0, verbose_name='类型')
    img = QiniuField(max_length=5000, blank=True, null=True, verbose_name='图片')

    class Meta:
        db_table = 'tb_issue_building_dynamic_message'
        verbose_name = '楼盘动态信息'
        managed = True
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.building_detial_id, self.author_id, self.title, self.content, self.message_create_time, self.author, self.id, self.img)

    def b_name(self):
        return self.building_detial.building_name

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>',self.img)
    b_name.short_description = '楼盘名称'
    image_data.short_description = u'楼盘图片'


class LandAuction(models.Model):
    '''土拍'''
    classfiy_name = models.ForeignKey(LandDistrict, on_delete=models.CASCADE, null=True, blank=True,  verbose_name='地区分类')
    RESIDENCE_CHOICES = ((1, '住宅'), (2, '商业'))
    if_residence = models.SmallIntegerField(choices=RESIDENCE_CHOICES, default=0, verbose_name='是否住宅')
    SALE_CHOICES = ((0, '已出让'), (1, '未出让'))
    if_sale = models.SmallIntegerField(choices=SALE_CHOICES, default=0, verbose_name='是否出让')
    land_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='地块名称')
    map = QiniuField(max_length=500, blank=True, null=True, verbose_name='地图')
    land_region = models.CharField(max_length=250, blank=True, null=True, verbose_name='地块区域')
    land_position = models.CharField(max_length=250, blank=True, null=True, verbose_name='宗地位置')
    nuddle_price = models.CharField(max_length=250, blank=True, null=True, verbose_name='楼面价')
    acquisition_company = models.CharField(max_length=200, blank=True, null=True, verbose_name='竞得方')
    start_parice = models.CharField(max_length=200, blank=True, null=True, verbose_name='起拍价')
    end_parice = models.CharField(max_length=200, blank=True, null=True, verbose_name='成交价')
    give_area = models.CharField(max_length=200, blank=True, null=True, verbose_name='出让面积')
    deal_all_price = models.CharField(max_length=200, blank=True, null=True, verbose_name='成交总价')
    max_volume_rate = models.CharField(max_length=200, blank=True, null=True, verbose_name='最大容积率')
    overflow = models.CharField(max_length=200, blank=True, null=True, verbose_name='溢价率')
    land_use = models.CharField(max_length=200, blank=True, null=True, verbose_name='土地用途')
    give_year = models.CharField(max_length=200, blank=True, null=True, verbose_name='出让年限')
    land_ask_for = models.CharField(max_length=50, blank=True, null=True, verbose_name='宗地要求')
    land_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='宗地编号')
    for_remark = models.CharField(max_length=50, blank=True, null=True, verbose_name='挂牌备注')
    long = models.FloatField(default=0,blank=True, null=True, verbose_name='经度')
    late = models.FloatField(default=0,blank=True, null=True, verbose_name='纬度')
    deal_date = models.CharField(max_length=100, blank=True, null=True, verbose_name='成交日期')
    land_img = QiniuField(max_length=500, blank=True, null=True, verbose_name='地块图片')
    create_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'tb_land_auction'
        verbose_name = '土拍'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.classfiy_name_id, self.land_name, self.map, self.land_region, self.land_position, self.nuddle_price, self.acquisition_company, self.start_parice, self.end_parice, self.give_area, self.deal_all_price, self.max_volume_rate, self.overflow, self.land_use, self.give_year, self.land_ask_for, self.land_number, self.deal_date)

    def b_name(self):
        return self.classfiy_name.name

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>',self.land_img)
    b_name.short_description = '分类'
    image_data.short_description = u'楼盘图片'


class PublicPlan(models.Model):
    '''公示方案'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘详情')
    autor = models.CharField(max_length=55, null=True, blank=True, verbose_name='作者')
    title = models.CharField(max_length=55, null=True, blank=True, verbose_name='标题')
    img = QiniuField(max_length=5000, null=True, blank=True, verbose_name='资料图片')
    two_title = models.CharField(max_length=55, null=True, blank=True, verbose_name='二级标题')
    content = RichTextUploadingField(null=True, blank=True, verbose_name='内容')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_public_plan'
        verbose_name = '楼盘选择类型'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.fk_id, self.title, self.img, self.id, self.two_title, self.content, self.autor)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '楼盘名称'

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>',self.img)
    image_data.short_description = u'楼盘图片'


class VRAerialPhotoAllPingImage(models.Model):
    '''VR/航拍/总平'''

    CHOICES = ((0, 'VR'), (1, '航拍'), (2, '总平'))
    choice_classfiy = models.SmallIntegerField(choices=CHOICES, default=0, verbose_name='图片类型')
    fuck = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, blank=True, null=True, verbose_name='楼盘详情')
    building_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='楼盘id')
    image_url = models.ImageField(blank=True, null=True, verbose_name='图片')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    IMAGE_CHOICES = ((0, 'no'), (1, 'yes'))
    if_vr = models.SmallIntegerField(choices=IMAGE_CHOICES, default=0, verbose_name='是否vr')
    if_aerial_photo = models.SmallIntegerField(choices=IMAGE_CHOICES, default=0, verbose_name='是否行拍')
    if_all_ping = models.SmallIntegerField(choices=IMAGE_CHOICES, default=0, verbose_name='是否总平')
    
    class Meta:
        db_table = 'tb_VR_aerial_photo_all_ping_image'
        verbose_name = 'VR/航拍/总平'
        managed = True
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.fuck_id, self.id, self.image_url, self.create_time, self.choice_classfiy, self.building_id)

    def b_name(self):
        return self.fuck.building_name
    b_name.short_description = '楼盘名称'

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.image_url,
        )
    image_data.short_description = u'楼盘图片'


class QuestionEveryProblem(models.Model):
    '''7组件(购房资料问题表)/摇号常见问题/公积金问题/征信打印指南/资料模板下载/资格查询/摇号流程/'''
    CHOICES_CLASSFIY = ((0, '摇号常见问题'), (1, '公积金问题'), (2, '征信打印指南'), (3, '资料模板下载'), (4, '资格查询'), (5, '摇号流程'))
    choice = models.SmallIntegerField(choices=CHOICES_CLASSFIY, default=0, verbose_name='分类')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='标题')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    img = QiniuField(max_length=5000, blank=True, null=True, verbose_name='图片')

    class Meta:
        db_table = 'tb_question_every_problem'
        verbose_name = '7组件'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.choice, self.create_time, self.title, self.id, self.content, self.img)

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.img,
        )
    image_data.short_description = u'资料图片'


class BuyHouseHundredDepartmentClassfiy(models.Model):
    """购房百科分类"""
    '''(无房资格查询)/人才政策/公积金政策/落户资格查询/购房流程/贷款办理/(资料模板)/落户指南/(带框计算)/房产证明/(购房资格查询)/社保及限购/新手引导'''
    name = models.CharField(max_length=50, verbose_name='名称')
    key_name = models.CharField(max_length=50, verbose_name='类别键名')

    class Meta:
        db_table = 'tb_buy_house_hundred_department_classfiy'
        verbose_name = '购房百科分类'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s' % (self.name, self.key_name, self.id)


class BuyHouseHundredDepartment(models.Model):
    '''购房百科'''
    classfiy = models.ForeignKey(BuyHouseHundredDepartmentClassfiy, on_delete=models.CASCADE, verbose_name='购房百科分类')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='标题')
    two_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='二级标题')
    text_img = QiniuField(max_length=500, blank=True, null=True, verbose_name='资料图片')
    text = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    create_time = models.DateTimeField(auto_now=True, verbose_name='问题创建时间')
    click_zan = models.IntegerField(default=0, verbose_name='点赞量')

    class Meta:
        db_table = 'tb_buy_house_hundred_department'
        verbose_name = '购房百科'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.id, self.title, self.two_title, self.text_img, self.text, self.create_time, self.classfiy_id, self.click_zan)

    def b_name(self):
        return self.classfiy.name
    b_name.short_description = '类别'

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.text_img,
        )

    image_data.short_description = u'资料图片'


class Article(models.Model):
    '''文章'''
    ARTICLE_CHOICES = ((0, '买房干货'), (1, '楼市解读'), (2, '楼市百科'), (3, '房产投资'))
    choice_classfiy = models.SmallIntegerField(choices=ARTICLE_CHOICES, default=0, verbose_name='文章分类')
    author = models.CharField(max_length=50, blank=True, null=True, verbose_name='作者')
    author_img = QiniuField(max_length=500, blank=True, null=True, verbose_name='作者头像')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name='标题')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    land = models.TextField(blank=True, null=True, verbose_name='地区')
    new_img = QiniuField(max_length=500, blank=True, null=True, verbose_name='图片')
    read = models.IntegerField(default=0, blank=True, null=True, verbose_name='阅读量')
    zanc = models.IntegerField(default=0, blank=True, null=True, verbose_name='点赞量')

    class Meta:
        db_table = 'tb_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.choice_classfiy, self.author, self.create_time, self.title, self.id, self.content, self.new_img)

    def image_data1(self):
        return format_html('<img src="{}" width="100px"/>', self.author_img)
    image_data1.short_description = u'头像'

    def image_data2(self):
        return format_html('<img src="{}" width="100px"/>', self.new_img)
    image_data2.short_description = u'图片'

class HouseImage(models.Model):
    '''户型图'''
    HOUSE_CHOICES = ((0, '一室一厅'), (1, '一室两厅'), (2, '两室一厅'), (3, '两室两厅'), (4, '三室一厅'), (5, '三室两厅'), (6, '四室一厅'), (7, '四室两厅'), (8, '五室一厅'), (9, '五室两厅'))
    choice_classfiy = models.SmallIntegerField(choices=HOUSE_CHOICES, default=0, verbose_name='户型样式')

    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘详情')

    image = models.TextField(max_length=5000, blank=True, null=True, verbose_name='图片')
    building_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='楼盘id') # 选择的楼盘为顾问添加的楼盘
    house_classfiy = models.CharField(max_length=100, blank=True, null=True, verbose_name='户型分类') # A1
    house_area = models.CharField(max_length=100, blank=True, null=True, verbose_name='建筑面积')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_house_image'
        verbose_name = '户型图'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.id, self.choice_classfiy, self.fk_id,  self.image, self.building_id, self.create_time, self.house_classfiy, self.house_area)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '类别'

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>', self.image)
    image_data.short_description = u'图片'


class BuildingImage(models.Model):
    '''楼盘相册'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘详情')

    HOUSE_CHOICES = ((0, '全部'), (1, '实景图'), (2, '项目周边'), (3, '样板间'), (4, '效果图'), (5, '鸟瞰图'))
    choice_classfiy = models.SmallIntegerField(choices=HOUSE_CHOICES, default=0, verbose_name='户型分类')

    photo_image = QiniuField(max_length=5000, blank=True, null=True, verbose_name='图片')
    create_time = models.DateField(auto_now=True,blank=True, null=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_building_image'
        verbose_name = '楼盘图片'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s ' % (self.fk_id, self.choice_classfiy, self.id, self.photo_image, self.create_time)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '类别'

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.photo_image,
        )
    image_data.short_description = u'楼盘图片'


class BuildingOneHouseOnePriceImage(models.Model):
    '''生成的一房一价图片'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘详情')
    photo_image = QiniuField(max_length=5000, blank=True, null=True, verbose_name='图片')
    create_time = models.DateField(auto_now=True,blank=True, null=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_building_one_house_one_price_image'
        verbose_name = '生成的一房一价图片'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (self.fk_id, self.id, self.photo_image, self.create_time)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '类别'

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.photo_image,
        )
    image_data.short_description = u'楼盘图片'


class BuildingVideo(models.Model):
    '''视频'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE, verbose_name='楼盘详情')

    HOUSE_CHOICES = ((0, '其他'), (1, '项目官方宣传'), (2, '项目周边讲解'), (3, '沙盘讲解'), (4, '样板间拍摄'))
    choice_classfiy = models.SmallIntegerField(choices=HOUSE_CHOICES, default=0, verbose_name='户型分类')
    video = QiniuField(max_length=5000, null=True, blank=True, verbose_name='视频')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_building_video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s ' % (self.fk_id, self.choice_classfiy, self.id, self.video, self.create_time)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '类别'

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>', self.video)
    image_data.short_description = u'图片'


class Share(models.Model):  # 搜索时以楼盘类别和我的关注作为筛选条件, 最新和最热分享
    '''分享堂'''
    middle_fk = models.ForeignKey('authorization.MiddlePeople', on_delete=models.CASCADE, verbose_name='置业顾问id')
    bd_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='顾问主营楼盘id')
    building_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='楼盘名称')
    mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name='手机号')
    author = models.CharField(max_length=25, blank=True, null=True, verbose_name='作者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    content = RichTextUploadingField(max_length=255, blank=True, null=True, verbose_name='内容')
    browse_count = models.IntegerField(default=0, blank=True, null=True, verbose_name='浏览量')
    img = QiniuField(max_length=500, blank=True, null=True, verbose_name='图片')
    video = QiniuField(max_length=500, blank=True, null=True, verbose_name='视频')
    HOUSE_CHOICES = ((0, '公寓'), (1, '住宅'))
    choice_classfiy = models.SmallIntegerField(choices=HOUSE_CHOICES, default=0, verbose_name='住宅类型分类')
    head_img = QiniuField(max_length=500, blank=True, null=True,verbose_name='头像')

    class Meta:
        db_table = 'tb_share'
        verbose_name = '分享堂'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.bd_id, self.middle_fk_id, self.id, self.create_time, self.content, self.img, self.video, self.author)

    def m_name(self):
        return self.middle_fk.nick_name
    m_name.short_description = '顾问名称'

    # def b_name(self):
    #     return self.building_fk.building_name
    # b_name.short_description = '所属楼盘'

    def image_data1(self):
        return format_html('<img src="{}" width="100px"/>', self.img)
    image_data1.short_description = u'图片'

    def image_data2(self):
        return format_html('<img src="{}" width="100px"/>', self.video)
    image_data2.short_description = u'视频'

    def image_data3(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    image_data3.short_description = u'头像'


class ZanCount(models.Model):
    '''点赞'''
    user_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户id')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    ZAN_CHOICES = ((0, '楼盘评论赞'), (1, '文章赞'), (2, '赞回答里面的答'), (3, '顾问里面的加赞'), (4, '购房百科的赞'))
    choice_classfiy = models.SmallIntegerField(choices=ZAN_CHOICES, default=0, verbose_name='点赞分类')
    type_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='需要点赞内容的id') # 主键id

    class Meta:
        db_table = 'tb_zan_count'
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s' % (
        self.id,  self.create_time,  self.choice_classfiy,
        self.user_id)


class Comment(models.Model):
    '''评论'''
    catgrage_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='所属id')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    click_count = models.IntegerField(default=0, verbose_name='点赞数')
    author_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='作者名称')
    author_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='作者id')
    village_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='楼盘id')
    title = models.CharField(max_length=20, blank=True, null=True, verbose_name='标题')
    content = RichTextUploadingField(max_length=255, blank=True, null=True, verbose_name='内容')
    head_img = QiniuField(max_length=255, blank=True, null=True, verbose_name='头像')

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.id, self.catgrage_id, self.author_name, self.village_id, self.create_time, self.click_count, self.content, self.title)

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    image_data.short_description = u'头像'


class Question(models.Model):
    '''问'''
    name = models.ForeignKey('authorization.Users', on_delete=models.CASCADE,blank=True, null=True, verbose_name='作者')
    author = models.CharField(max_length=30, blank=True, null=True, verbose_name='作者')
    author_id = models.CharField(max_length=30, blank=True, null=True, verbose_name='作者ID')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    title = models.CharField(max_length=30, blank=True, null=True, verbose_name='标题')
    q_type = models.CharField(max_length=15, blank=True, null=True, verbose_name='类型')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    browse_count = models.IntegerField(default=0, verbose_name='浏览量')
    answer_count = models.IntegerField(default=0, verbose_name='回答量')
    head_img = QiniuField(max_length=255, blank=True, null=True, verbose_name='头像')

    QUESTION_CHOICES = ((0, '无'), (1, '已回答'), (2, '已解决'), (3, '未回答'))
    choice_classfiy = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='解决状态')

    STATUS_CHOICES = ((0, '无'), (1, '落户'), (2, '社保'), (3, '刚需'), (4, '限购'))
    buy_house_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='购房资格')

    TOU_CHOICES = ((0, '无'), (1, '城市规划'), (2, '楼盘对比'), (3, '房价预测'))
    tou_choice = models.SmallIntegerField(choices=TOU_CHOICES, default=0, verbose_name='投资指南')

    BUY_SALE_CHOICES = ((0, '无'), (1, '交易过户'), (2, '公积金'), (3, '贷款'))
    buy_sale_choice = models.SmallIntegerField(choices=BUY_SALE_CHOICES, default=0, verbose_name='买房卖房')

    DECORATION_CHOICES = ((0, '无'), (1, '精装'), (2, '毛胚'))
    decoration_choice = models.SmallIntegerField(choices=DECORATION_CHOICES, default=0, verbose_name='装修')


    class Meta:
        db_table = 'tb_question'
        verbose_name = '问'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.author, self.create_time, self.title, self.browse_count, self.answer_count, self.choice_classfiy, self.buy_house_status, self.tou_choice, self.buy_sale_choice, self.decoration_choice )

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    image_data.short_description = u'头像'


class Answer(models.Model):
    '''答'''
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, verbose_name='问题')
    com = models.CharField(max_length=255, null=True, blank=True, verbose_name='评论id')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    aut = models.TextField(blank=True, null=True, verbose_name='作者')
    aut_id = models.TextField(blank=True, null=True, verbose_name='作者id')
    head_img = QiniuField(max_length=255, blank=True, null=True, verbose_name='头像')
    click_count = models.IntegerField(default=0, verbose_name='点赞数')
    catgrage_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='点评所属id') # 默认没有

    class Meta:
        db_table = 'tb_answer'
        verbose_name = '答'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.question_id, self.aut, self.create_time, self.click_count, self.id, self.click_count)

    def b_name(self):
        return self.question.title
    b_name.short_description = '问题'

    def image_data(self):
        return format_html('<img src="{}" width="100px"/>', self.head_img)
    image_data.short_description = u'头像'


class UserAnswerBuilding(models.Model):
    '''楼盘回复'''
    author = models.ForeignKey('authorization.Users', on_delete=models.CASCADE, verbose_name='作者')
    building_detial = models.CharField(max_length=255, blank=True, null=True, verbose_name='楼盘名称')
    com = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='楼盘评论id')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    title = models.CharField(max_length=20, verbose_name='标题')
    content = RichTextUploadingField(max_length=255, verbose_name='内容')
    click_count = models.IntegerField(default=0, verbose_name='点赞数')

    class Meta:
        db_table = 'tb_user_answer_building'
        verbose_name = '楼盘回复'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.author_id, self.building_detial,self.com_id, self.id, self.create_time, self.title, self.content, self.click_count)

    def a_name(self):
        return self.author.nick_name
    a_name.short_description = '作者'

    def b_name(self):
        return self.com.id
    b_name.short_description = '所属问题id'


class OtherImg(models.Model):
    '''其他图片'''
    feedback_classfiy = QiniuField(max_length=5000, blank=True, null=True, verbose_name='服务号')
    buy_house_qun = QiniuField(max_length=5000, blank=True, null=True, verbose_name='买房群')
    feedback_img = QiniuField(max_length=5000, blank=True, null=True, verbose_name='公众号')

    class Meta:
        db_table = 'tb_question_other_img'
        verbose_name = '其他图片'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s ' % (self.feedback_classfiy, self.buy_house_qun, self.feedback_img, self.id)

    def image_data1(self):
        return format_html('<img src="{}" width="100px"/>', self.feedback_classfiy)
    image_data1.short_description = u'服务号'

    def image_data2(self):
        return format_html('<img src="{}" width="100px"/>', self.buy_house_qun)
    image_data2.short_description = u'买房群'

    def image_data3(self):
        return format_html('<img src="{}" width="100px"/>', self.feedback_img)
    image_data3.short_description = u'公众号'


class SystemMessage(models.Model):
    '''系统消息'''
    fk = models.ForeignKey(BuildingDetial, on_delete=models.CASCADE,blank=True, null=True, verbose_name='楼盘详情')

    title = models.CharField(max_length=30, blank=True, null=True, verbose_name='标题')
    bd_id = models.CharField(max_length=30, blank=True, null=True, verbose_name='楼盘id')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='内容')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_system_message'
        verbose_name = '系统消息'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.fk_id, self.bd_id, self.id, self.title, self.content, self.create_time)

    def b_name(self):
        return self.fk.building_name
    b_name.short_description = '楼盘'
    

class WinPKHistory(models.Model):
    '''成功竞价记录'''
    fk = models.ForeignKey('authorization.MiddlePeople', on_delete=models.CASCADE, blank=True, null=True, verbose_name='顾问')
    QUESTION_CHOICES = ((1, '轮播图'), (2, '首页广告位'), (3, '详情页广告位'))
    choice_classfiy = models.SmallIntegerField(choices=QUESTION_CHOICES, default=0, verbose_name='类型')
    building_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='准备上楼盘详情页的id')
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name='成交金额')
    create_time = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='数据创建时间')

    class Meta:
        db_table = 'tb_win_pk_history'
        verbose_name = '成功竞价记录'
        verbose_name_plural = verbose_name
        managed = True

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.fk_id, self.choice_classfiy, self.id, self.price, self.building_id, self.create_time)

    def b_name(self):
        return self.fk.really_name
    b_name.short_description = '顾问'
