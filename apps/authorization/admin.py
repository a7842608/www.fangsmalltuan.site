from django.contrib import admin

# Register your models here.
from authorization.models import AttentionVillage, ReallyNameMiddlePeopleShare, UserHistoryMessageRecord, \
    MiddlePeopleHistoryMessageRecord, WhoLookMiddelPeople, GaoBuildingDetialPKMoney, GaoIndexPKMoney, \
    IntegralSubsidiary, GoldenMoney, MyWeChat, ExclusiveCustmer, MyPhoneCall, QuestionFeedback, MiddlePeople, \
    UserCodeNumber, UserLotteryNumber, Users, AttentionAretical, AttentionMiddlePeople, WhoZanMiddelPeople, \
    AttentionMiddlePeopleVillage

admin.site.site_header = '仿小团'
admin.site.site_title = '仿小团MIS'
admin.site.index_title = '欢迎使用仿小团MIS'


@admin.register(AttentionMiddlePeopleVillage) # 顾问关注的楼盘
class AttentionMiddlePeopleVillageAdmin(admin.ModelAdmin):
    list_per_page = 10 # 每页显示几条
    actions_on_top = True # 顶部显示
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'building_id', 'user_id'] # 发布列


@admin.register(AttentionVillage) # 用户关注的楼盘
class AttentionVillageAdmin(admin.ModelAdmin):
    list_per_page = 10 # 每页显示几条
    actions_on_top = True # 顶部显示
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'building_id', 'user_id'] # 发布列


@admin.register(AttentionMiddlePeople) # 用户关注的置业顾问
class AttentionMiddlePeopleAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'middle_people_id', 'user_id']  # 发布列


@admin.register(AttentionAretical)  # 用户关注的文章
class AttentionAreticalAdmin(admin.ModelAdmin):
    list_per_page = 10 # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'aretical_id', 'user_id']  # 发布列

# ?
@admin.register(Users)  # 用户
class UsersAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'nick_name', 'mobile']  # 发布列


@admin.register(UserLotteryNumber)  # 用户摇号
class UserLotteryNumberAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'b_name', 'number', 'really_name', 'create_time']  # 发布列


@admin.register(UserCodeNumber)  # 用户编码
class UserCodeNumberAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'b_name', 'number', 'really_name', 'create_time']  # 发布列

# ?
@admin.register(MiddlePeople)  # 置业顾问
class MiddlePeopleAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'create_time']  # 发布列


@admin.register(QuestionFeedback)  # 问题反馈
class QuestionFeedbackAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'choice_classfiy', 'my_create_time', 'my_content', 'feedback_phone', 'image1', 'image2']  # 发布列


@admin.register(MyPhoneCall)  # 我的来电
class MyPhoneCallAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'header_img', 'choice_classfiy', 'name', 'user_id', 'phone_time', 'user_phone',  'create_time']  # 发布列


@admin.register(ExclusiveCustmer)  # 专属客户
class ExclusiveCustmerAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'header_img', 'user_id', 'user_name', 'custmer_time', 'create_time']  # 发布列


@admin.register(MyWeChat)  # 我的微聊
class MyWeChatAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'header_img', 'user_id', 'user_name', 'custmer_time', 'where_come_from', 'choice_classfiy', 'create_time']  # 发布列


@admin.register(GoldenMoney)  # 金币明细表
class GoldenMoneyAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'money_count', 'recharge_time', 'change_beacuse', 'choice_classfiy', 'create_time']  # 发布列


@admin.register(IntegralSubsidiary)  # 积分明细表
class IntegralSubsidiaryAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'score', 'score_create_time', 'change_beacuse', 'choice_classfiy','create_time']  # 发布列


@admin.register(GaoIndexPKMoney)  # 首页广告竞价
class GaoIndexPKMoneyAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'building_id', 'price', 'create_time']  # 发布列


@admin.register(GaoBuildingDetialPKMoney)  # 楼盘详情页竞价
class GaoBuildingDetialPKMoneyAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'building_id', 'price', 'create_time']  # 发布列


@admin.register(WhoLookMiddelPeople)  # 顾问访客
class WhoLookMiddelPeopleAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'user_id', 'create_time']  # 发布列


@admin.register(WhoZanMiddelPeople)  # 用户点赞了顾问
class WhoZanMiddelPeopleAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'user_id', 'middle_id', 'create_time']  # 发布列


# @admin.register(MiddlePeopleHistoryMessageRecord)  # 顾问历史消息记录
# class MiddlePeopleHistoryMessageRecordAdmin(admin.ModelAdmin):
#     list_per_page = 10  # 每页显示几条
#     actions_on_top = True  # 顶部显示
#     search_fields = ['id']  # 搜索框
#     list_display = ['id', 'u_name', 'user_id', 'middle_id', 'content', 'create_time']  # 发布列


# @admin.register(UserHistoryMessageRecord)  # 用户历史消息记录
# class UserHistoryMessageRecordAdmin(admin.ModelAdmin):
#     list_per_page = 10  # 每页显示几条
#     actions_on_top = True  # 顶部显示
#     search_fields = ['id']  # 搜索框
#     list_display = ['id', 'u_name', 'user_id', 'middle_id', 'content', 'create_time']  # 发布列


@admin.register(ReallyNameMiddlePeopleShare)  # 获客神器
class ReallyNameMiddlePeopleShareAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'u_name', 'user_id', 'middle_id', 'name', 'create_time']  # 发布列
