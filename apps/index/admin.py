from django.contrib import admin

from index.models import LandDistrict, Subway, SubwayStation, BuildingClassfiy, BuildingDetial, HistoryLottery, \
    OneHouseOnePrice, BuildingStatueTimeSale, ToldPurpose, IssueBuildingDynamicMessage, LandAuction, PublicPlan, \
    SystemMessage, OtherImg, UserAnswerBuilding, Answer, Question, Comment, Share, BuildingVideo, BuildingImage, \
    HouseImage, Article, BuyHouseHundredDepartment, BuyHouseHundredDepartmentClassfiy, QuestionEveryProblem, \
    VRAerialPhotoAllPingImage, ZanCount

admin.site.site_header = '仿小团'
admin.site.site_title = '仿小团MIS'
admin.site.index_title = '欢迎使用仿小团MIS'


@admin.register(LandDistrict) # 地区
class LandDistrictAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    list_filter = ['name'] # 右侧过滤栏
    search_fields = ['name'] # 搜索框
    list_display = ['id', 'name', 'key_name'] # 发布列


@admin.register(Subway) # 地铁
class SubwayAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    list_filter = ['name'] # 右侧过滤栏
    search_fields = ['name'] # 搜索框
    list_display = ['id', 'name', 'key_name'] # 发布列


@admin.register(SubwayStation) # 地铁站
class SubwayAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    list_filter = ['name']  # 右侧过滤栏
    search_fields = ['name']  # 搜索框
    list_display = ['suby_name', 'suby_id', 'name', 'id'] # 发布列


@admin.register(BuildingClassfiy) # 楼盘其他类型
class BuildingClassfiyAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    # actions_on_bottom = True # 底部显示
    list_filter = ['name']  # 右侧过滤栏
    search_fields = ['name']  # 搜索框
    list_display = ['id', 'name']  # 发布列


# ?
@admin.register(BuildingDetial) # 楼盘详情
class BuildingDetialAdmin(admin.ModelAdmin):
    list_per_page = 50 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    list_filter = ['building_name'] # 右侧过滤栏
    search_fields = ['building_name'] # 搜索框
    list_display = ['id', 'building_name', ] # 发布列

# ?
@admin.register(HistoryLottery) # 历史摇号信息
class HistoryLotteryAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    # list_filter = ['name'] # 右侧过滤栏
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'detial_id','name', 'one_price', 'all_price', 'decorate_situation', 'house', 'cool_captial_request', 'house_count', 'people_count', 'win_probability'] # 发布列


# @admin.register(OneHouseOnePrice) # 一房一价
# class OneHouseOnePriceAdmin(admin.ModelAdmin):
#     list_per_page = 15 # 每页显示几条
#     actions_on_top = True # 顶部显示
#     # actions_on_bottom = True # 底部显示
#     # list_filter = [''] # 右侧过滤栏
#     search_fields = ['id'] # 搜索框
#     list_display = ['building_detial_id', 'house_dong', 'house_yuan',  'house_ceng', 'door_number', 'if_sale', 'classfiy', 'one_price', 'all_price'] # 发布列


@admin.register(BuildingStatueTimeSale) # 楼盘销售时间
class BuildingStatueTimeSaleAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    # list_filter = ['name'] # 右侧过滤栏
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'b_name', 'will_sale_time', 'register_time', 'commit_time', 'want_told_time', 'lottery_time', 'choice_house_time'] # 发布列


@admin.register(ToldPurpose) # 意向登记表/摇号结果
class ToldPurposeAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    # actions_on_bottom = True # 底部显示
    # list_filter = ['name'] # 右侧过滤栏
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'b_name', 'lottery_name', 'ID_number', 'audit_status', 'if_win_lottery', 'create_time'] # 发布列


@admin.register(IssueBuildingDynamicMessage) # (发表)楼盘动态信息(房小团官宣)
class IssueBuildingDynamicMessageAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'b_name', 'title', 'content', 'author',  'author_id', 'message_create_time', 'choice_classfiy', 'image_data']  # 发布列


@admin.register(LandAuction) # 土拍
class LandAuctionAdmin(admin.ModelAdmin):
    list_per_page = 15 # 每页显示几条
    actions_on_top = True # 顶部显示
    search_fields = ['id'] # 搜索框
    list_display = ['id', 'b_name', 'if_residence', 'if_sale', 'land_name',  'map', 'land_region', 'land_position', 'nuddle_price', 'acquisition_company', 'start_parice', 'end_parice','give_area', 'deal_all_price', 'max_volume_rate', 'overflow', 'land_use', 'give_year', 'land_ask_for', 'land_number', 'for_remark', 'long', 'late', 'deal_date', 'image_data']  # 发布列


@admin.register(PublicPlan) # 公示方案
class PublicPlanAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'autor', 'title', 'two_title', 'content', 'create_time', 'image_data'] # 发布列


@admin.register(VRAerialPhotoAllPingImage) # VR/航拍/总平
class VRAerialPhotoAllPingImageAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'if_vr', 'if_aerial_photo', 'if_all_ping', 'create_time', 'image_data']  # 发布列


@admin.register(QuestionEveryProblem) # 7组件
class QuestionEveryProblemAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    # search_fields = ['id']  # 搜索框
    list_display = ['id', 'choice', 'create_time', 'title', 'content', 'image_data']  # 发布列


@admin.register(BuyHouseHundredDepartmentClassfiy) # 购房百科分类
class BuyHouseHundredDepartmentClassfiyAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'name', 'key_name']  # 发布列


@admin.register(BuyHouseHundredDepartment) # 购房百科
class BuyHouseHundredDepartmentAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'title', 'two_title', 'text', 'click_zan', 'create_time', 'image_data']  # 发布列


@admin.register(Article) # 文章
class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'choice_classfiy', 'author', 'image_data1', 'create_time', 'title', 'content', 'land', 'image_data2']  # 发布列


@admin.register(HouseImage) # 户型图
class HouseImageAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'choice_classfiy', 'b_name', 'building_id', 'house_classfiy', 'house_area', 'image_data', 'create_time']  # 发布列


@admin.register(BuildingImage) # 楼盘相册
class BuildingImageAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'choice_classfiy', 'image_data', 'create_time']


@admin.register(BuildingVideo) # 视频
class BuildingVideoAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'choice_classfiy', 'image_data', 'create_time']


# @admin.register(Share) # 分享堂
# class ShareAdmin(admin.ModelAdmin):
#     list_per_page = 15 # 每页显示几条
#     actions_on_top = True  # 顶部显示
#     search_fields = ['id']  # 搜索框
#     list_display = ['id', 'b_name', 'm_name','image_data3', 'classfiy', 'building_name', 'author', 'content', 'choice_classfiy', 'browse_count', 'image_data1', 'image_data2', 'create_time']

# ?
@admin.register(ZanCount) # 点赞
class ZanCountAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'user_id', 'type_id', 'choice_classfiy', 'create_time']

# ?
@admin.register(Comment) # 评论
class CommentAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'catgrage_id', 'author_name',  'author_id',  'village_id',  'title',  'content',  'image_data', 'click_count', 'create_time']


@admin.register(Question) # 问
class QuestionAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'author','choice_classfiy', 'title', 'buy_house_status', 'tou_choice', 'buy_sale_choice', 'decoration_choice', 'browse_count','answer_count', 'create_time']


@admin.register(Answer) # 答
class AnswerAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'aut', 'content', 'image_data', 'click_count', 'create_time']


@admin.register(UserAnswerBuilding) # 楼盘回复
class UserAnswerBuildingAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'a_name', 'b_name', 'building_detial', 'title', 'content', 'click_count', 'create_time']


@admin.register(OtherImg) # 其他图片
class OtherImgAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'image_data1', 'image_data2', 'image_data3']


@admin.register(SystemMessage) # 系统消息
class SystemMessageAdmin(admin.ModelAdmin):
    list_per_page = 15  # 每页显示几条
    actions_on_top = True  # 顶部显示
    search_fields = ['id']  # 搜索框
    list_display = ['id', 'b_name', 'title', 'content', 'create_time']
