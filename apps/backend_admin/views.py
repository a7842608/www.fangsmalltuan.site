import json

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.base import View

from backend_admin.models import AccountExecutive
from authorization.models import MiddlePeople, Users, AttentionVillage, GaoBuildingDetialPKMoney, WhoZanMiddelPeople, \
    MiddlePeopleHistoryMessageRecord, WhoLookMiddelPeople, MyPhoneCall, ExclusiveCustmer, ReallyNameMiddlePeopleShare, \
    GoldenMoney, IntegralSubsidiary, AttentionMiddlePeopleVillage, UserLoginRecord, UserLoginBuildingRecord, \
    UserHistoryMessageRecord, UserLotteryNumber, AttentionAretical, AttentionMiddlePeople, UserCodeNumber, \
    QuestionFeedback, GaoIndexPKMoney, UserSealStatus, SensitiveWord, MaxConnectionAndMaxPeopleAndMaxCountView
from index.models import BuildingDetial, BuildingImage, IssueBuildingDynamicMessage, HouseImage, BuildingVideo, \
    VRAerialPhotoAllPingImage, LandDistrict, OneHouseOnePrice, HistoryLottery, ToldPurpose, Comment, \
    BuildingStatueTimeSale, Article, BuyHouseHundredDepartment, BuyHouseHundredDepartmentClassfiy, LandAuction, Share, \
    SystemMessage, WinPKHistory, SubwayStation, Subway, BuildingClassfiy, Question, LotteryResult, UnionLotteryResult
from template_message.models import MessageTemplateValue


class AdminBackendLogin(View):
    '''用户登录'''

    def post(self, request):
        try:
            # 1.接收三个参数
            username = request.POST.get('username')
            password = request.POST.get('password')
            rank = request.POST.get('rank')

            req = AccountExecutive.objects.get(choice_classfiy=0)

            # if username != req.user_name and password != req.password:

            # if user_name, password != req.user_name, req.password:

            if username != req.user_name:
                return JsonResponse({'Code': 400, 'Errmsg': '账号错误'})
            elif password != req.password:
                return JsonResponse({'Code': 400, 'Errmsg': '密码错误'})
            else:
                return JsonResponse({"statue": 200, 'data': 'success'}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialSearchView(View):
    '''楼盘搜索框'''

    def get(self, request):
        try:
            bd = request.GET.get('bd_value')
            req = BuildingDetial.objects.values().filter(building_name__contains=bd)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                json_dict['only_id'] = i['id']  # 唯一id
                json_dict['building_name'] = i['building_name']  # 楼盘名称
                json_dict['sale_stage'] = i['sale_stage']  # 销售状态
                json_dict['ave_price'] = i['unit_price']  # 均价??
                json_dict['premises_location'] = i['premises_location']  # 地区
                json_dict['unit_price'] = i['unit_price']  # 参考单价
                json_dict['open_name'] = i['building_name']  # 开盘名称
                json_dict['decorate_situation'] = i['decorate_situation']  # 装修
                json_dict['open_house_number'] = i['open_house_number']  # 销售范围
                json_dict['open_house_section'] = i['open_house_section']  # 主力户型
                json_dict['cool_captial_request'] = i['cool_captial_request']  # 验资金额
                json_dict['registration_way'] = i['registration_way']  # 报名方式
                json_dict['building_nickname'] = i['building_nickname']  # 别名
                json_dict['upstart'] = i['upstart']  # 开发商
                json_dict['will_sale_number'] = i['will_sale_number']  # 预售证号
                json_dict['house_section'] = i['open_house_section']  # 户型区间
                json_dict['covered_classfiy'] = i['covered_classfiy']  # 物业类型
                json_dict['green_rate'] = i['green_rate']  # 绿化率
                json_dict['equity_year'] = i['equity_year']  # 产权年限
                json_dict['volume_rate'] = i['volume_rate']  # 容积率
                json_dict['delivery_time'] = i['delivery_time']  # 交房时间
                json_dict['stall_message'] = i['stall_message']  # 交房时间
                json_dict['floor_space'] = i['floor_space']  # 占地面积
                json_dict['covered_area'] = i['covered_area']  # 建筑面积
                json_dict['cube_count'] = i['cube_count']  # 整栋数
                json_dict['company_money'] = i['company_money']  # 物业费
                json_dict['all_house_count'] = i['all_house_count']  # 总户数
                json_dict['company'] = i['company']  # 物业公司
                json_dict['premises_location'] = i['premises_location']  # 楼盘地址
                json_dict['tier_condition'] = i['tier_condition']  # 楼层情况
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingXiaLaView(View):
    '''楼盘下拉菜单'''

    def get(self, request):
        try:
            data = request.GET.get('val')
            if data != '楼盘下拉菜单':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = BuildingDetial.objects.values().all().order_by('-create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['bd_id'] = i['id']
                json_dict['building_name'] = i['building_name']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingListPageView(View):
    '''楼盘列表页'''

    def get(self, request):
        try:
            data = request.GET.get('val')
            if data != '楼盘列表':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = BuildingDetial.objects.values().all().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = BuildingDetial.objects.all().count()
                json_dict['all_count'] = count
                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                ld = i['land_id']
                lld = LandDistrict.objects.filter(id=ld).values('name')
                for bbb in list(lld):
                    json_dict['land'] = bbb
                json_dict['bd_id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['sale_building_location'] = i['sale_building_location']
                json_dict['unit_price'] = i['unit_price']  # 参考单价
                json_dict['decorate_situation'] = i['decorate_situation']  # 装修
                json_dict['open_house_number'] = i['open_house_number']  # 销售范围
                json_dict['open_house_section'] = i['open_house_section']  # 主力户型
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['registration_way'] = i['registration_way']  # 报名方式
                json_dict['will_sale_number'] = i['will_sale_number']  # 预售证号
                json_dict['house_section'] = i['open_house_section']  # 户型区间
                json_dict['stall_message'] = i['stall_message']  # 交房时间
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘列表页筛选框'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict['page']
            del json_dict['page']
            # req = BuildingDetial.objects.values(cd).order_by('-create_time')
            req = BuildingDetial.objects.filter(**json_dict).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(bd)
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = BuildingDetial.objects.all().count()
                json_dict['all_count'] = count
                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                ld = i['land_id']
                lld = LandDistrict.objects.filter(id=ld).values('name')
                for bbb in list(lld):
                    json_dict['land'] = bbb
                json_dict['bd_id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['sale_building_location'] = i['sale_building_location']
                json_dict['unit_price'] = i['unit_price']  # 参考单价
                json_dict['decorate_situation'] = i['decorate_situation']  # 装修
                json_dict['open_house_number'] = i['open_house_number']  # 销售范围
                json_dict['open_house_section'] = i['open_house_section']  # 主力户型
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['registration_way'] = i['registration_way']  # 报名方式
                json_dict['will_sale_number'] = i['will_sale_number']  # 预售证号
                json_dict['house_section'] = i['open_house_section']  # 户型区间
                json_dict['stall_message'] = i['stall_message']  # 交房时间
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialView(View):
    '''楼盘详情/查'''

    def get(self, request):
        try:
            bd = request.GET.get('bd_id')
            req = BuildingDetial.objects.values().filter(id=bd)
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['land'] = i['land_id']
                json_dict['train'] = i['train_id']
                json_dict['budling_other'] = i['budling_other_id']
                json_dict['only_id'] = i['id']  # 唯一id
                json_dict['building_name'] = i['building_name']
                json_dict['total_price'] = i['total_price']
                json_dict['unit_price'] = i['unit_price']
                json_dict['house_section'] = i['house_section']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['sale_stage_time'] = i['sale_stage_time']
                json_dict['sale_building_location'] = i['sale_building_location']
                json_dict['premises_location'] = i['premises_location']
                json_dict['delivery_time'] = i['delivery_time']
                json_dict['longitude'] = i['longitude']
                json_dict['latitude'] = i['latitude']
                json_dict['building_nickname'] = i['building_nickname']
                json_dict['building_classfiy'] = i['building_classfiy']
                json_dict['equity_year'] = i['equity_year']
                json_dict['green_rate'] = i['green_rate']
                json_dict['volume_rate'] = i['volume_rate']
                json_dict['stall_message'] = i['stall_message']
                json_dict['cube_count'] = i['cube_count']
                json_dict['all_house_count'] = i['all_house_count']
                json_dict['floor_space'] = i['floor_space']
                json_dict['covered_area'] = i['covered_area']
                json_dict['covered_classfiy'] = i['covered_classfiy']
                json_dict['covered_tier'] = i['covered_tier']
                json_dict['company'] = i['company']
                json_dict['company_money'] = i['company_money']
                json_dict['upstart'] = i['upstart']
                json_dict['tier_condition'] = i['tier_condition']
                json_dict['train_traffic'] = i['train_traffic']
                json_dict['bus_site'] = i['bus_site']
                json_dict['school'] = i['school']
                json_dict['bank'] = i['bank']
                json_dict['catering'] = i['catering']
                json_dict['hospital'] = i['hospital']
                json_dict['shopping'] = i['shopping']
                json_dict['park'] = i['park']
                json_dict['other_mating'] = i['other_mating']
                json_dict['building_intro'] = i['building_intro']
                json_dict['if_index_advertising'] = i['if_index_advertising']
                json_dict['if_lunbo_choice'] = i['if_lunbo_choice']
                json_dict['if_building_detail_advertising'] = i['if_building_detail_advertising']
                json_dict['attention_degree'] = i['attention_degree']
                json_dict['comment_count'] = i['comment_count']
                json_dict['open_house_number'] = i['open_house_number']
                json_dict['open_price'] = i['open_price']
                json_dict['decorate_situation'] = i['decorate_situation']
                json_dict['open_house_section'] = i['open_house_section']
                json_dict['open_house_count'] = i['open_house_count']
                json_dict['registration_way'] = i['registration_way']
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['house_count'] = i['house_count']
                json_dict['people_count'] = i['people_count']
                json_dict['win_probability'] = i['win_probability']
                json_dict['will_sale_number'] = i['will_sale_number']
                json_dict['give_number_time'] = i['give_number_time']
                json_dict['lottery_count'] = i['lottery_count']
                json_dict['building_create_time'] = i['building_create_time']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘详情/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            BuildingDetial.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialADDView(View):
    '''楼盘/添加'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingDetial.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialDelView(View):
    '''楼盘详情/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                BuildingDetial.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingImageView(View):
    '''楼盘图片/查/改'''

    def get(self, request):  # 分类查询
        try:
            cf = request.GET.get('choice')
            bd = request.GET.get('bd_id')
            req = BuildingImage.objects.filter(Q(choice_classfiy=cf) & Q(fk_id=bd)).values('id', 'fk_id',
                                                                                           'choice_classfiy',
                                                                                           'photo_image', 'create_time')
            query = list(req)
            # paginator = Paginator(query, 5)
            # page = int(request.GET.get('page'))
            # try:
            #     page_value = paginator.page(page)
            # except EmptyPage:
            #     return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in query:
                json_dict = {}
                count = BuildingImage.objects.filter().count()
                count2 = BuildingImage.objects.filter(Q(choice_classfiy=cf) & Q(fk_id=bd)).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['photo_image'] = i['photo_image']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)  #

    '''楼盘图片/修改'''  # 需要调用七牛云

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            BuildingImage.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)  #


class BuildingImageCreateView(View):
    '''楼盘图片/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingImage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingImageDelView(View):
    '''楼盘图片/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                BuildingImage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingVideoView(View):
    '''楼盘视频/查'''

    def get(self, request):  # 分类查询
        try:
            cf = request.GET.get('choice')
            bd = request.GET.get('bd_id')
            req = BuildingVideo.objects.filter(Q(choice_classfiy=cf) & Q(fk_id=bd)).values('id', 'fk_id',
                                                                                           'choice_classfiy', 'video',
                                                                                           'create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = BuildingVideo.objects.filter().count()
                count2 = BuildingVideo.objects.filter(Q(choice_classfiy=cf) & Q(fk_id=bd)).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['video'] = i['video']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)  #

    '''楼盘视频/修改'''  # 需要调用七牛云

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            BuildingVideo.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)  #


class BuildingVideoCreateView(View):
    '''楼盘视频/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingVideo.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingVideoDelView(View):
    '''楼盘视频/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                BuildingVideo.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingStatueMessageView(View):
    '''楼盘动态信息/查'''

    def get(self, request):
        try:
            # cf = request.GET.get('choice')
            bd = request.GET.get('bd_id')
            req = IssueBuildingDynamicMessage.objects.filter(building_detial_id=bd).values('id', 'building_detial_id',
                                                                                           'title', 'content',
                                                                                           'message_create_time',
                                                                                           'author', 'author_id',
                                                                                           'choice_classfiy', 'img')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = IssueBuildingDynamicMessage.objects.filter().count()
                count2 = IssueBuildingDynamicMessage.objects.filter(building_detial_id=bd).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['building_detial_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['title'] = i['title']
                json_dict['author'] = i['author']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['img'] = i['img']
                json_dict['message_create_time'] = i['message_create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘动态信息/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            IssueBuildingDynamicMessage.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingStatueMessageCreateView(View):
    '''楼盘动态信息详情/查'''

    def get(self, request):
        try:
            bd = request.GET.get('bd_id')
            req = IssueBuildingDynamicMessage.objects.filter(id=bd).values()
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['building_detial_id']
                # b = BuildingDetial.objects.get(id=a)
                # json_dict['building_name'] = b.building_name
                json_dict['title'] = i['title']
                json_dict['author'] = i['author']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['img'] = i['img']
                json_dict['message_create_time'] = i['message_create_time']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘动态信息/发表'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            IssueBuildingDynamicMessage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingStatueMessageDelView(View):
    '''楼盘动态信息/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                IssueBuildingDynamicMessage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingHouseImageView(View):
    '''楼盘户型图'''

    def get(self, request):  # 分类查询
        try:
            cf = request.GET.get('choice')
            bd = request.GET.get('bd_id')
            req = HouseImage.objects.filter(Q(choice_classfiy=cf) & Q(fk_id=bd)).values('id', 'fk_id',
                                                                                        'choice_classfiy', 'image',
                                                                                        'house_classfiy', 'house_area',
                                                                                        'create_time')
            query = list(req)
            # paginator = Paginator(query, 10)
            # page = int(request.GET.get('page'))
            # try:
            #     page_value = paginator.page(page)
            # except EmptyPage:
            #     return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in query:
                json_dict = {}
                count = HouseImage.objects.filter().count()
                count2 = HouseImage.objects.filter(Q(choice_classfiy=cf) & Q(fk_id=bd)).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['house_classfiy'] = i['house_classfiy']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['house_area'] = i['house_area']
                json_dict['img'] = i['image']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)  #

    '''楼盘户型图/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            HouseImage.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingHouseImageCreateView(View):
    '''楼盘户型图/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            HouseImage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingHouseImageDelView(View):
    '''楼盘户型图/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                HouseImage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneHouseOnePriceView(View):
    '''一房一价/查'''

    def get(self, request):
        try:
            bd = request.GET.get('bd_id')
            req = OneHouseOnePrice.objects.filter(building_detial=bd).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = OneHouseOnePrice.objects.filter().count()
                count2 = OneHouseOnePrice.objects.filter(building_detial=bd).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['building_detial_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['house_dong'] = i['house_dong']
                json_dict['house_yuan'] = i['house_yuan']
                json_dict['create_area'] = i['create_area']
                json_dict['door_number'] = i['door_number']
                json_dict['create_area'] = i['create_area']
                json_dict['in_area'] = i['in_area']
                json_dict['gave_house'] = i['gave_house']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['will_sale_number'] = i['will_sale_number']
                json_dict['public_date'] = i['public_date']
                json_dict['give_date'] = i['give_date']
                json_dict['build_company'] = i['build_company']
                json_dict['lottery_title'] = i['lottery_title']
                json_dict['create_time'] = i['create_time']
                # json_dict['will_sale_number'] = i['will_sale_number']
                # json_dict['water_money'] = i['water_money']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''一房一价/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            OneHouseOnePrice.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneHouseOnePriceCreateView(View):
    '''一房一价总数据已匹配'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '一房一价总数据已匹配':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            total_page = OneHouseOnePrice.objects.exclude(building_detial_id__isnull=True).count()
            first = OneHouseOnePrice.objects.exclude(building_detial_id__isnull=True).values('lottery_title').distinct()
            paginator = Paginator(first, 10)
            page = int(request.GET.get('page') or '1')
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            first_query = list(page_value)
            data_list = []

            for one in first_query:
                jd1 = {}
                jd1['label'] = one['lottery_title']
                # 1号楼#151#2020-11-30#商贸,写字楼#杭政储出[2017]54号#杭售许字(2020)第000134号
                second = OneHouseOnePrice.objects.filter(lottery_title=one['lottery_title']).values('will_sale_number',
                                                                                                    'house_dong',
                                                                                                    'all_tao_count',
                                                                                                    'give_date',
                                                                                                    'house_use',
                                                                                                    'lottery_title').distinct()
                second_list = list(second)
                print(second_list)
                data_list1 = []
                for two in second_list:
                    jd2 = {}
                    thred = OneHouseOnePrice.objects.filter(
                        Q(will_sale_number=two['will_sale_number']) & Q(house_dong=two['house_dong'])).values('id',
                                                                                                              'door_number',
                                                                                                              'in_area',
                                                                                                              'gave_house',
                                                                                                              'one_price',
                                                                                                              'all_price',
                                                                                                              'public_date',
                                                                                                              'build_company',
                                                                                                              'will_sale_number',
                                                                                                              'create_time',
                                                                                                              'building_detial_id')
                    thred_list = list(thred)
                    jd2['house_dong'] = two['house_dong']
                    jd2['all_tao_count'] = two['all_tao_count']
                    jd2['give_date'] = two['give_date']
                    jd2['house_use'] = two['house_use']
                    jd2['lottery_title'] = two['lottery_title']
                    jd2['will_sale_number'] = two['will_sale_number']
                    jd2['children'] = thred_list
                    data_list1.append(jd2)
                jd1['children'] = data_list1
                data_list.append(jd1)
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''一房一价/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            OneHouseOnePrice.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneHouseOnePriceDelView(View):
    '''一房一价总数据未匹配'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '一房一价总数据未匹配':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            total_page = OneHouseOnePrice.objects.filter(building_detial_id__isnull=True).count()
            first = OneHouseOnePrice.objects.filter(building_detial_id__isnull=True).values('lottery_title').distinct()
            paginator = Paginator(first, 10)
            page = int(request.GET.get('page') or '1')
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for one in page_value:
                jd1 = {}
                jd1['label'] = one['lottery_title']
                # 1号楼#151#2020-11-30#商贸,写字楼#杭政储出[2017]54号#杭售许字(2020)第000134号
                second = OneHouseOnePrice.objects.filter(lottery_title=one['lottery_title']).values('will_sale_number',
                                                                                                    'house_dong',
                                                                                                    'all_tao_count',
                                                                                                    'give_date',
                                                                                                    'house_use',
                                                                                                    'lottery_title').distinct()
                second_list = list(second)
                print(second_list)
                data_list1 = []
                for two in second_list:
                    jd2 = {}
                    thred = OneHouseOnePrice.objects.filter(
                        Q(will_sale_number=two['will_sale_number']) & Q(house_dong=two['house_dong'])).values('id',
                                                                                                              'door_number',
                                                                                                              'in_area',
                                                                                                              'gave_house',
                                                                                                              'one_price',
                                                                                                              'all_price',
                                                                                                              'public_date',
                                                                                                              'build_company',
                                                                                                              'will_sale_number',
                                                                                                              'create_time',
                                                                                                              'building_detial_id')
                    thred_list = list(thred)
                    jd2['house_dong'] = two['house_dong']
                    jd2['all_tao_count'] = two['all_tao_count']
                    jd2['give_date'] = two['give_date']
                    jd2['house_use'] = two['house_use']
                    jd2['lottery_title'] = two['lottery_title']
                    jd2['will_sale_number'] = two['will_sale_number']
                    jd2['children'] = thred_list
                    data_list1.append(jd2)
                jd1['children'] = data_list1
                data_list.append(jd1)
            return JsonResponse({"statue": 200, 'data': data_list, 'count': paginator.num_pages}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)

    '''一房一价/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                OneHouseOnePrice.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class VRFlyAllImageView(View):
    '''vr/航拍/总评 - 查'''

    def get(self, request):  # 分类查询
        try:
            cf = request.GET.get('choice')
            bd = request.GET.get('bd_id')
            req = VRAerialPhotoAllPingImage.objects.filter(Q(choice_classfiy=cf) & Q(fuck_id=bd)).values('id',
                                                                                                         'fuck_id',
                                                                                                         'choice_classfiy',
                                                                                                         'image_url',
                                                                                                         'create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = VRAerialPhotoAllPingImage.objects.filter().count()
                count2 = VRAerialPhotoAllPingImage.objects.filter(Q(choice_classfiy=cf) & Q(fuck_id=bd)).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['fuck_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['image_url'] = i['image_url']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''vr/航拍/总评-修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            VRAerialPhotoAllPingImage.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class VRFlyAllImageCreateView(View):  # ?
    '''总vr/航拍/总总评 - 查'''

    def get(self, request):  # 分类查询
        try:
            cf = request.GET.get('choice')
            req = VRAerialPhotoAllPingImage.objects.filter(choice_classfiy=cf).values('id', 'fuck_id',
                                                                                      'choice_classfiy', 'image_url',
                                                                                      'create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = VRAerialPhotoAllPingImage.objects.filter().count()
                count2 = VRAerialPhotoAllPingImage.objects.filter(choice_classfiy=cf).count()
                json_dict['all_count'] = count
                json_dict['choice_count'] = count2
                json_dict['id'] = i['id']
                a = i['fuck_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['bd_id'] = a
                json_dict['image_url'] = i['image_url']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''VR/户型/总评上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            VRAerialPhotoAllPingImage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class VRFlyAllImageDelView(View):
    '''总摇号数据/未匹配'''

    def get(self, request):
        try:
            bd = request.GET.get('val')
            if bd != '未匹配总摇号数据':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = UnionLotteryResult.objects.filter(fk_id__isnull=True).values('pid', 'fk_id',
                                                                               'building_name').order_by('-create_time')
            query = list(req)
            allc = len(query)
            data_list = []
            for i in query[0:10]:
                json_dict = {}
                json_dict['pid'] = i['pid']
                json_dict['building_name'] = i['building_name']
                json_dict['build_count'] = allc
                a = LotteryResult.objects.filter(pid=i['pid']).values('pid', 'serial_number', 'buy_house_number',
                                                                      'create_time').order_by('-serial_number')[0:10]
                co = LotteryResult.objects.filter(pid=i['pid']).count()
                if co > 100:
                    ab = list(a)[0:101]
                else:
                    ab = list(a)
                json_dict['values_count'] = co
                json_dict['data'] = ab
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''vr/航拍/总评-删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                VRAerialPhotoAllPingImage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HistoryLotteryMessageView(View):
    '''历史摇号信息/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('bd_id')
            req = HistoryLottery.objects.filter(detial_id=bd).values().order_by('-lottery_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count2 = HistoryLottery.objects.filter(detial_id=bd).count()
                json_dict['choice_count'] = count2
                a = i['detial_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['lottery_time'] = i['lottery_time']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['decorate_situation'] = i['decorate_situation']
                json_dict['house'] = i['house']
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['house_count'] = i['house_count']
                json_dict['people_count'] = i['people_count']
                json_dict['win_probability'] = i['win_probability']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''历史摇号信息/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            HistoryLottery.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HistoryLotteryMessageCreateView(View):
    '''总摇号数据/已匹配'''

    def get(self, request):
        try:
            bd = request.GET.get('val')
            if bd != '已匹配总摇号数据':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = UnionLotteryResult.objects.filter(fk_id__isnull=False).values('pid', 'fk_id').order_by('-create_time')
            query = list(req)
            allc = len(query)
            data_list = []
            for i in query:
                json_dict = {}
                aa = i['fk_id']
                b = BuildingDetial.objects.get(id=aa)
                json_dict['building_name'] = b.building_name
                json_dict['build_count'] = allc
                a = LotteryResult.objects.filter(pid=i['pid']).values('pid', 'serial_number', 'buy_house_number',
                                                                      'create_time').order_by('-serial_number')
                co = LotteryResult.objects.filter(pid=i['pid']).count()
                ab = list(a)
                json_dict['values_count'] = co
                json_dict['data'] = ab
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''历史摇号信息/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            HistoryLottery.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HistoryLotteryMessageDelView(View):
    '''历史摇号信息/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                HistoryLottery.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IntentToRegisterView(View):
    '''意向登记/查'''

    def get(self, request):
        try:
            bd = request.GET.get('bd_id')
            req = ToldPurpose.objects.filter(fk_id=bd).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count2 = ToldPurpose.objects.filter(fk_id=bd).count()
                json_dict['choice_count'] = count2
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['buy_house_number'] = i['buy_house_number']
                json_dict['lottery_name'] = i['lottery_name']
                json_dict['ID_number'] = i['ID_number']
                json_dict['house_classfiy'] = i['house_classfiy']
                json_dict['find_number'] = i['find_number']
                json_dict['other_lottery_name'] = i['other_lottery_name']
                json_dict['other_ID_number'] = i['other_ID_number']
                json_dict['audit_status'] = i['audit_status']
                json_dict['if_win_lottery'] = i['if_win_lottery']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''意向登记/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            ToldPurpose.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IntentToRegisterSearchView(View):
    '''意向登记搜索框'''

    def get(self, request):
        try:
            bd = request.GET.get('asv')  # 预售证号
            req = ToldPurpose.objects.filter(building_name__contains=bd).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count2 = ToldPurpose.objects.filter(village_name_id=bd).count()
                json_dict['choice_count'] = count2
                a = i['village_name_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['buy_house_number'] = i['buy_house_number']
                json_dict['lottery_name'] = i['lottery_name']
                json_dict['ID_number'] = i['ID_number']
                json_dict['house_classfiy'] = i['house_classfiy']
                json_dict['find_number'] = i['find_number']
                json_dict['other_lottery_name'] = i['other_lottery_name']
                json_dict['other_ID_number'] = i['other_ID_number']
                json_dict['audit_status'] = i['audit_status']
                json_dict['if_win_lottery'] = i['if_win_lottery']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''总摇号数据/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                LotteryResult.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


# 获取已匹配总意向登记
class IntentToRegisterCreateView(View):
    '''已匹配总意向登记/查'''

    def get(self, request):
        try:
            bd = request.GET.get('val')
            if bd != '已匹配总意向登记':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            # start 开始修改
            req = UnionLotteryResult.objects.filter(fk_id__isnull=False).values('pid', 'fk_id', 'building_name',
                                                                                'id').order_by('-create_time')
            # end 开始修改
            query = list(req)
            allc = len(query)
            data_list = []
            for i in query:
                json_dict = {}
                aa = i['fk_id']
                b = BuildingDetial.objects.get(id=aa)
                json_dict['building_name'] = b.building_name
                json_dict['build_count'] = allc
                # start 开始修改
                json_dict['union_id'] = i['id']
                json_dict['union_name'] = i['building_name']
                # end 开始修改
                a = ToldPurpose.objects.filter(pid=i['pid']).values('id', 'pid', 'buy_house_number', 'lottery_name',
                                                                    'ID_number', 'house_classfiy', 'other_lottery_name',
                                                                    'other_ID_number', 'audit_status',
                                                                    'if_win_lottery').order_by('-create_time')
                co = ToldPurpose.objects.filter(pid=i['pid']).count()
                ab = list(a)
                json_dict['values_count'] = co
                json_dict['data'] = ab
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''意向登记/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode('utf-8'))
            ToldPurpose.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IntentToRegisterDelView(View):
    '''获取pid关联楼盘名称'''

    def get(self, request):
        try:
            # start 开始修改
            req = UnionLotteryResult.objects.filter(fk_id__isnull=False).values().order_by('create_time')
            # end 开始修改
            query = list(req)
            allc = len(query)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['building_name'] = i['building_name']
                json_dict['fk_id'] = i['fk_id']
                json_dict['id'] = i['id']
                json_dict['pid'] = i['pid']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''意向登记/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                ToldPurpose.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class EnterBuildingMiddlePeopleView(View):
    '''入驻的置业顾问/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('bd_id')
            i0 = AttentionMiddlePeopleVillage.objects.filter(building_id=bd).values('user_id')
            ili = list(i0)
            data_list = []
            for ii in ili:
                t = ii['user_id']
                req = MiddlePeople.objects.filter(id=t).values().order_by('-create_time')
                query = list(req)
                paginator = Paginator(query, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                for i in page_value:
                    json_dict = {}
                    count = MiddlePeople.objects.filter(building_fk_id=bd).count()
                    json_dict['all_count'] = count
                    a = i['building_fk_id']
                    b = BuildingDetial.objects.get(id=a)
                    json_dict['building_name'] = b.building_name
                    json_dict['id'] = i['id']
                    json_dict['nick_name'] = i['nick_name']
                    json_dict['mobile'] = i['mobile']
                    json_dict['header_img'] = i['header_img']
                    json_dict['really_name'] = i['really_name']
                    json_dict['ID_card'] = i['ID_card']
                    json_dict['wechat_number'] = i['wechat_number']
                    json_dict['rank'] = i['rank']
                    json_dict['bussiness_building'] = i['bussiness_building']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['live_limit'] = i['live_limit']
                    json_dict['click_count'] = i['click_count']
                    json_dict['call_mobile'] = i['call_mobile']
                    json_dict['wechat_talk'] = i['wechat_talk']
                    json_dict['exclusive_people'] = i['exclusive_people']
                    json_dict['integral'] = i['integral']
                    json_dict['golden_money'] = i['golden_money']
                    json_dict['give_price_history'] = i['give_price_history']
                    json_dict['invitation_code'] = i['invitation_code']
                    json_dict['two_wei_ma'] = i['two_wei_ma']
                    json_dict['work_pai'] = i['work_pai']
                    # json_dict['chat_room'] = i['chat_room']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''入驻的置业顾问/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            MiddlePeople.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class EnterBuildingMiddlePeopleCreateView(View):
    '''未匹配总意向登记/查'''

    def get(self, request):
        try:
            bd = request.GET.get('val')
            if bd != '未匹配总意向登记':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = UnionLotteryResult.objects.filter(fk_id__isnull=True).values('id', 'pid', 'building_name').order_by(
                '-create_time')
            query = list(req)
            allc = len(query)
            data_list = []
            for i in query[0:10]:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['pid'] = i['pid']
                json_dict['building_name'] = i['building_name']
                json_dict['build_count'] = allc
                a = ToldPurpose.objects.filter(pid=i['pid']).values('id', 'pid', 'buy_house_number', 'lottery_name',
                                                                    'ID_number', 'house_classfiy', 'other_lottery_name',
                                                                    'other_ID_number', 'audit_status',
                                                                    'if_win_lottery').order_by('-create_time')[0:10]
                co = ToldPurpose.objects.filter(pid=i['pid']).count()
                if co > 100:
                    ab = list(a)[0:101]
                else:
                    ab = list(a)
                json_dict['values_count'] = co
                json_dict['data'] = ab
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''入驻的置业顾问/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            AttentionMiddlePeopleVillage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class EnterBuildingMiddlePeopleDelView(View):
    '''入驻的置业顾问/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                MiddlePeople.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AttentionBuildingUsersView(View):
    '''关注该楼盘的用户/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('bd_id')
            uid = AttentionVillage.objects.filter(building_id=bd).values('user_id')
            a = []
            for i in uid:
                a.append(i['user_id'])
            req = Users.objects.filter(id__in=a).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                bb = i['id']
                count = AttentionVillage.objects.filter(building_id=bd).count()
                json_dict['all_count'] = len(a)
                json_dict['id'] = i['id']
                json_dict['open_id'] = i['open_id']
                json_dict['user_uuid'] = i['user_uuid']
                json_dict['nick_name'] = i['nick_name']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['really_name'] = i['really_name']
                json_dict['adreess'] = i['adreess']
                json_dict['ID_card'] = i['ID_card']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['middle_id'] = i['middle_id']
                json_dict['create_time'] = i['create_time']
                json_dict['if_middle_people'] = i['if_middle_people']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''关注该楼盘的用户/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            Users.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AttentionBuildingUsersCreateView(View):
    '''关注该楼盘的用户/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            AttentionVillage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AttentionBuildingUsersDelView(View):
    '''关注该楼盘的用户/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Users.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingCommentView(View):
    '''楼盘评论/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('bd_id')
            req = Comment.objects.filter(village_id=bd).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Comment.objects.filter(village_id=bd).count()
                json_dict['all_count'] = count
                a = i['village_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['head_img'] = i['head_img']
                json_dict['content'] = i['content']
                json_dict['title'] = i['title']
                json_dict['author_name'] = i['author_name']
                json_dict['click_count'] = i['click_count']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘评论/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            Comment.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingCommentCreateView(View):
    '''总楼盘评论数据'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('val')
            if mp != '总楼盘评论数据':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Comment.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Comment.objects.all().count()
                json_dict['all_count'] = count
                a = i['village_id']
                b = BuildingDetial.objects.filter(id=a).values('building_name')
                for k in b:
                    json_dict['building_name'] = k['building_name']
                json_dict['id'] = i['id']
                json_dict['head_img'] = i['head_img']
                json_dict['content'] = i['content']
                json_dict['title'] = i['title']
                json_dict['author_name'] = i['author_name']
                json_dict['click_count'] = i['click_count']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘评论/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Comment.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingCommentDelView(View):
    '''楼盘评论/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Comment.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingSaleTimeView(View):
    '''楼盘销售时间/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('bd_id')
            req = BuildingStatueTimeSale.objects.filter(fk_id=bd).values()
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = BuildingStatueTimeSale.objects.filter(fk_id=bd).count()
                json_dict['all_count'] = count
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['will_sale_time'] = i['will_sale_time']
                json_dict['register_time'] = i['register_time']
                json_dict['commit_time'] = i['commit_time']
                json_dict['want_told_time'] = i['want_told_time']
                json_dict['lottery_time'] = i['lottery_time']
                json_dict['choice_house_time'] = i['choice_house_time']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘销售时间/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            BuildingStatueTimeSale.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingSaleTimeCreateView(View):
    '''总楼盘销售时间/查'''

    def get(self, request):
        try:
            bd = request.GET.get('val')
            if bd != '总楼盘销售时间':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = BuildingStatueTimeSale.objects.all().values().order_by('fk_id')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = BuildingStatueTimeSale.objects.all().count()
                json_dict['all_count'] = count
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['will_sale_time'] = i['will_sale_time']
                json_dict['register_time'] = i['register_time']
                json_dict['commit_time'] = i['commit_time']
                json_dict['want_told_time'] = i['want_told_time']
                json_dict['lottery_time'] = i['lottery_time']
                json_dict['choice_house_time'] = i['choice_house_time']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'page': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘销售时间/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingStatueTimeSale.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingSaleTimeDelView(View):
    '''楼盘销售时间/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                BuildingStatueTimeSale.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialPKView(View):
    '''楼盘详情页竞价/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('bd_id')
            req = GaoBuildingDetialPKMoney.objects.filter(building_id=bd).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = GaoBuildingDetialPKMoney.objects.filter(building_id=bd).count()
                json_dict['all_count'] = count
                a = i['building_id']
                b = BuildingDetial.objects.get(id=a)
                aa = i['fk_id']
                bb = MiddlePeople.objects.get(id=aa)
                json_dict['middle_name'] = bb.really_name
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['price'] = i['price']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘详情页竞价/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            GaoBuildingDetialPKMoney.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialPKCreateView(View):
    '''总楼盘详情页竞价/查'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('val')
            if bd != '总楼盘详情页竞价':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = GaoBuildingDetialPKMoney.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = GaoBuildingDetialPKMoney.objects.all().count()
                json_dict['all_count'] = count
                a = i['building_id']
                b = BuildingDetial.objects.get(id=a)
                aa = i['fk_id']
                bb = MiddlePeople.objects.get(id=aa)
                json_dict['middle_name'] = bb.really_name
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['price'] = i['price']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘详情页竞价/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            GaoBuildingDetialPKMoney.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialPKDelView(View):
    '''楼盘详情页竞价/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                GaoBuildingDetialPKMoney.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class WillSaleCardView(View):
    '''预售证'''

    def get(self, request):
        try:
            bd = request.GET.get('bd_id')
            req = BuildingDetial.objects.filter(id=bd).values('id', 'building_name', 'will_sale_number',
                                                              'give_number_time', 'lottery_count',
                                                              'building_create_time', 'create_time', 'upstart',
                                                              'company')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = BuildingDetial.objects.filter(id=bd).count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['will_sale_number'] = i['will_sale_number']
                json_dict['give_number_time'] = i['give_number_time']
                json_dict['lottery_count'] = i['lottery_count']
                json_dict['building_create_time'] = i['building_create_time']
                json_dict['create_time'] = i['create_time']
                json_dict['upstart'] = i['upstart']
                json_dict['company'] = i['company']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleSearchView(View):
    '''顾问搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('mpv')
            req = MiddlePeople.objects.values().filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['nick_name'] = i['nick_name']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['invitation_code'] = i['invitation_code']
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['browse_count'] = i['browse_count']
                json_dict['live_limit'] = i['live_limit']
                json_dict['click_count'] = i['click_count']
                json_dict['integral'] = i['integral']
                json_dict['golden_money'] = i['golden_money']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    def post(self, request):
        try:
            ifm = request.POST.get('if_mp_id')
            req = Users.objects.filter(if_middle_people=ifm).values('id', 'really_name')
            query = list(req)
            return JsonResponse({"statue": 200, 'data': query}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleListView(View):
    '''顾问列表页'''

    def get(self, request):
        try:
            mp = request.GET.get('mpl')
            if mp != '顾问列表':
                return JsonResponse({'statue': 400, 'data': 'value_fale'})
            req = MiddlePeople.objects.values().all().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = MiddlePeople.objects.count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['nick_name'] = i['nick_name']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['invitation_code'] = i['invitation_code']
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['browse_count'] = i['browse_count']
                json_dict['live_limit'] = i['live_limit']
                json_dict['click_count'] = i['click_count']
                json_dict['integral'] = i['integral']
                json_dict['rank'] = i['rank']
                json_dict['golden_money'] = i['golden_money']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleBasicInformationView(View):
    '''顾问基本信息/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = MiddlePeople.objects.filter(id=mp).values().order_by('-create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['room_number'] = i['room_number']
                json_dict['nick_name'] = i['nick_name']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['personal_introduce'] = i['personal_introduce']
                json_dict['really_name'] = i['really_name']
                json_dict['ID_card'] = i['ID_card']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['rank'] = i['rank']
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['browse_count'] = i['browse_count']
                json_dict['live_limit'] = i['live_limit']
                json_dict['click_count'] = i['click_count']
                json_dict['call_mobile'] = i['call_mobile']
                json_dict['wechat_talk'] = i['wechat_talk']
                json_dict['exclusive_people'] = i['exclusive_people']
                json_dict['integral'] = i['integral']
                json_dict['golden_money'] = i['golden_money']
                json_dict['invitation_code'] = i['invitation_code']
                json_dict['two_wei_ma'] = i['two_wei_ma']
                json_dict['work_pai'] = i['work_pai']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问基本信息/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            MiddlePeople.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleBasicInformationCreateView(View):
    '''顾问详情页'''

    def get(self, request):
        try:
            mp = request.GET.get('mp_id')
            req = MiddlePeople.objects.values().filter(id=mp).order_by('-create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = MiddlePeople.objects.count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['nick_name'] = i['nick_name']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['really_name'] = i['really_name']
                json_dict['ID_card'] = i['ID_card']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['invitation_code'] = i['invitation_code']
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['browse_count'] = i['browse_count']
                json_dict['live_limit'] = i['live_limit']
                json_dict['click_count'] = i['click_count']
                json_dict['integral'] = i['integral']
                json_dict['golden_money'] = i['golden_money']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问基本信息/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            MiddlePeople.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleBasicInformationDelView(View):
    '''顾问基本信息/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                MiddlePeople.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleClickZanRecordView(View):
    '''顾问点赞记录/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = WhoZanMiddelPeople.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = WhoZanMiddelPeople.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['user_id'] = i['user_id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问点赞记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            WhoZanMiddelPeople.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleClickZanRecordCreateView(View):
    '''顾问点赞记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            WhoZanMiddelPeople.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleClickZanRecordDelView(View):
    '''顾问点赞记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                WhoZanMiddelPeople.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleChatRecordView(View):
    '''顾问聊天记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('mp_id')
            req = MiddlePeopleHistoryMessageRecord.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = MiddlePeopleHistoryMessageRecord.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问点赞记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            MiddlePeopleHistoryMessageRecord.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleChatRecordCreateView(View):
    '''总顾问聊天数据/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '总顾问聊天数据':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = MiddlePeopleHistoryMessageRecord.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = MiddlePeopleHistoryMessageRecord.objects.all().count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问点赞记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            MiddlePeopleHistoryMessageRecord.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleChatRecordDelView(View):
    '''顾问点赞记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                MiddlePeopleHistoryMessageRecord.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleCustmerRecordView(View):
    '''顾问访客记录/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = WhoLookMiddelPeople.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = WhoLookMiddelPeople.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['user_id'] = i['user_id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问访客记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            WhoLookMiddelPeople.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleCustmerRecordCreateView(View):
    '''顾问访客记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            WhoLookMiddelPeople.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleCustmerRecordDelView(View):
    '''顾问访客记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                WhoLookMiddelPeople.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleComeMobileRecordView(View):
    '''顾问来电记录/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = MyPhoneCall.objects.filter(middle_people_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = MyPhoneCall.objects.filter(middle_people_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['phone_time'] = i['phone_time']
                json_dict['user_phone'] = i['user_phone']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问来电记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            MyPhoneCall.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleComeMobileRecordCreateView(View):
    '''顾问来电记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            MyPhoneCall.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleComeMobileRecordDelView(View):
    '''顾问来电记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                MyPhoneCall.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleExclusiveCustmerRecordView(View):
    '''顾问专属客户记录/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = ExclusiveCustmer.objects.filter(middle_name_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = ExclusiveCustmer.objects.filter(middle_name_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['custmer_time'] = i['custmer_time']
                # json_dict['user_phone'] = i['user_phone']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问来电记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            ExclusiveCustmer.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleExclusiveCustmerRecordCreateView(View):
    '''顾问专属客户记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            ExclusiveCustmer.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleExclusiveCustmerRecordDelView(View):
    '''顾问专属客户记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                ExclusiveCustmer.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGetCustmerGodMachineRecordView(View):
    '''顾问获客神器记录/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = ReallyNameMiddlePeopleShare.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = ReallyNameMiddlePeopleShare.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['come'] = i['name']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问获客神器记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            ReallyNameMiddlePeopleShare.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGetCustmerGodMachineRecordCreateView(View):
    '''顾问获客神器记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            ReallyNameMiddlePeopleShare.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGetCustmerGodMachineRecordDelView(View):
    '''顾问获客神器记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                ReallyNameMiddlePeopleShare.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGoldenRecordView(View):
    '''顾问金币表记录/查'''

    def get(self, request):  # 分类查询
        try:
            mp = request.GET.get('mp_id')
            req = GoldenMoney.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = GoldenMoney.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                d = MiddlePeople.objects.get(id=mp)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['money_count'] = i['money_count']
                json_dict['recharge_time'] = i['recharge_time']
                json_dict['change_beacuse'] = i['change_beacuse']
                json_dict['create_time'] = i['create_time']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问金币表记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            GoldenMoney.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGoldenRecordCreateView(View):
    '''顾问金币表记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            GoldenMoney.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGoldenRecordDelView(View):
    '''顾问金币表记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                GoldenMoney.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleScoreRecordView(View):
    '''顾问积分记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('mp_id')
            req = IntegralSubsidiary.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = IntegralSubsidiary.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                d = MiddlePeople.objects.get(id=mp)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['id'] = i['id']
                json_dict['score'] = i['score']
                json_dict['score_create_time'] = i['score_create_time']
                json_dict['change_beacuse'] = i['change_beacuse']
                json_dict['create_time'] = i['create_time']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问积分记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            IntegralSubsidiary.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleScoreRecordCreateView(View):
    '''顾问积分记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            IntegralSubsidiary.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleScoreRecordDelView(View):
    '''顾问积分记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                IntegralSubsidiary.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGoToHouseRecordView(View):
    '''顾问入住楼盘记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('mp_id')
            req = AttentionMiddlePeopleVillage.objects.filter(user_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = AttentionMiddlePeopleVillage.objects.filter(user_id=mp).count()
                json_dict['all_count'] = count
                d = BuildingDetial.objects.get(id=mp)
                json_dict['building_name'] = d.building_name
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''顾问入住楼盘记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            AttentionMiddlePeopleVillage.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGoToHouseCreateView(View):
    '''顾问入住楼盘记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            AttentionMiddlePeopleVillage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleGoToHouseDelView(View):
    '''顾问入住楼盘记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                AttentionMiddlePeopleVillage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


# ?
class MiddlePeopleRankRecordView(View):
    '''顾问等级记录/查'''
    pass


class UsersSearchView(View):
    '''用户搜索框'''

    def get(self, request):
        try:
            bd = request.GET.get('uv')
            req = SubwayStation.objects.filter(key_name__icontains=bd).values('id','name', 'key_name', 'create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})

            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': [i for i in page_value], 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)

    '''用户列表页'''

    def post(self, request):
        try:
            bd = request.POST.get('ul')
            if bd != '用户列表':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Users.objects.values().all().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.POST.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Users.objects.all().count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['mobile'] = i['mobile']
                json_dict['nick_name'] = i['nick_name']
                json_dict['really_name'] = i['really_name']
                json_dict['header_img'] = i['header_img']
                json_dict['adreess'] = i['adreess']
                json_dict['ID_card'] = i['ID_card']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['middle_id'] = i['middle_id']
                json_dict['create_time'] = i['create_time']
                json_dict['if_middle_people'] = i['if_middle_people']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersBasicInformationRecordView(View):
    '''用户基本信息/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = Users.objects.filter(id=mp).values().order_by('-create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['open_id'] = i['open_id']
                json_dict['user_uuid'] = i['user_uuid']
                json_dict['nick_name'] = i['nick_name']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['personal_introduce'] = i['personal_introduce']
                json_dict['adreess'] = i['adreess']
                json_dict['really_name'] = i['really_name']
                json_dict['ID_card'] = i['ID_card']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['middle_id'] = i['middle_id']
                json_dict['create_time'] = i['create_time']
                json_dict['if_middle_people'] = i['if_middle_people']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户基本信息/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            Users.objects.filter(id=bd).update(**json_dict)

            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersBasicInformationCreateView(View):
    '''用户基本信息/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Users.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersBasicInformationDelView(View):
    '''用户基本信息/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Users.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLoginRecordView(View):
    '''用户登陆记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = UserLoginRecord.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = UserLoginRecord.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['user_name'] = i['user_name']
                json_dict['header_img'] = i['header_img']
                json_dict['mobile'] = i['mobile']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户登陆记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            UserLoginRecord.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLoginCreateView(View):
    '''用户登陆记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            UserLoginRecord.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLoginDelView(View):
    '''用户登陆记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                UserLoginRecord.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLookBuildingRecordView(View):
    '''用户访问楼盘记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = UserLoginBuildingRecord.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = UserLoginBuildingRecord.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['user_name'] = i['user_name']
                json_dict['header_img'] = i['header_img']
                json_dict['mobile'] = i['mobile']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户访问楼盘记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            UserLoginBuildingRecord.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLookBuildingCreateView(View):
    '''用户访问楼盘记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            UserLoginBuildingRecord.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLookBuildingDelView(View):
    '''用户访问楼盘记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                UserLoginBuildingRecord.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersChatRecordView(View):
    '''用户聊天记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = UserHistoryMessageRecord.objects.filter(fk_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = UserHistoryMessageRecord.objects.filter(fk_id=mp).count()
                json_dict['all_count'] = count
                a = i['fk_id']
                d = Users.objects.get(id=a)
                json_dict['name'] = d.really_name
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['content'] = i['content']
                json_dict['header_img'] = d.header_img
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户聊天记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            UserHistoryMessageRecord.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersChatCreateView(View):
    '''用户聊天记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            UserHistoryMessageRecord.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersChatDelView(View):
    '''用户聊天记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                UserHistoryMessageRecord.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLotteryRecordView(View):
    '''用户摇号数据记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = UserLotteryNumber.objects.filter(user_id_id=mp).values().order_by('-create_time')
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                count = UserLotteryNumber.objects.filter(user_id_id=mp).count()
                json_dict['all_count'] = count
                a = i['user_id_id']
                d = Users.objects.get(id=a)
                c = i['build_id_id']
                b = BuildingDetial.objects.get(id=c)
                json_dict['building_name'] = b.building_name
                json_dict['header_img'] = d.header_img
                json_dict['name'] = d.really_name
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['number'] = i['number']
                json_dict['bd_id'] = c
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户摇号数据记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            UserLotteryNumber.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLotteryCreateView(View):
    '''用户摇号数据记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            UserLotteryNumber.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersLotteryDelView(View):
    '''用户摇号数据记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                UserLotteryNumber.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionArticalRecordView(View):
    '''用户关注的文章记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = AttentionAretical.objects.filter(user_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = AttentionAretical.objects.filter(user_id=mp).count()
                json_dict['all_count'] = count
                a = i['aretical_id']
                d = Article.objects.get(id=a)
                json_dict['title'] = d.title
                json_dict['author'] = d.author
                json_dict['author_img'] = d.author_img
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户关注的文章记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            AttentionAretical.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionArticalCreateView(View):
    '''用户关注的文章记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            AttentionAretical.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionArticalDelView(View):
    '''用户关注的文章记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                AttentionAretical.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionBuildingRecordView(View):
    '''用户关注的楼盘记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = AttentionVillage.objects.filter(user_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = AttentionVillage.objects.filter(user_id=mp).count()
                json_dict['all_count'] = count
                a = i['building_id']
                d = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = d.building_name
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户关注的楼盘记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            AttentionVillage.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionBuildingCreateView(View):
    '''用户关注的楼盘记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            AttentionVillage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionBuildingDelView(View):
    '''用户关注的楼盘记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                AttentionVillage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionMiddlePeopleRecordView(View):
    '''用户关注的置业顾问记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = AttentionMiddlePeople.objects.filter(user_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = AttentionMiddlePeople.objects.filter(user_id=mp).count()
                json_dict['all_count'] = count
                a = i['middle_people_id']
                d = MiddlePeople.objects.get(id=a)
                json_dict['really_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['wechat_number'] = d.wechat_number
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户关注的置业顾问记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            AttentionMiddlePeople.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionMiddlePeopleCreateView(View):
    '''用户关注的置业顾问记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            AttentionMiddlePeople.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersAttentionMiddlePeopleDelView(View):
    '''用户关注的置业顾问记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                AttentionMiddlePeople.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersCodeRecordView(View):
    '''用户编码记录/查'''

    def get(self, request):
        try:
            mp = request.GET.get('ur_id')
            req = UserCodeNumber.objects.filter(user_id_id=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = UserCodeNumber.objects.filter(user_id=mp).count()
                json_dict['all_count'] = count
                a = i['build_id_id']
                d = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = d.building_name
                json_dict['id'] = i['id']
                json_dict['really_name'] = i['really_name']
                json_dict['number'] = i['number']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''用户编码记录/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            UserCodeNumber.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersCodeCreateView(View):
    '''用户编码记录/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            UserCodeNumber.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UsersCodeDelView(View):
    '''用户编码记录/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                UserCodeNumber.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ProblemFeedbackView(View):
    '''问题反馈/查'''

    def get(self, request):
        try:
            mp = request.GET.get('pfv')
            if mp != '问题反馈':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = QuestionFeedback.objects.all().values().order_by('-my_create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = QuestionFeedback.objects.all().count()
                json_dict['all_count'] = count
                a = i['user_id']
                try:
                    d = Users.objects.get(id=a)
                except Exception as e:
                    return JsonResponse({"statue": 404, 'errmsg': str(e)})
                json_dict['really_name'] = d.really_name
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['id'] = i['id']
                json_dict['my_create_time'] = i['my_create_time']
                json_dict['my_content'] = i['my_content']
                json_dict['question_img'] = i['question_img']
                json_dict['feedback_phone'] = i['feedback_phone']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''问题反馈/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            QuestionFeedback.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ProblemFeedbackCreateView(View):
    '''问题反馈/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            QuestionFeedback.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ProblemFeedbackDelView(View):
    '''问题反馈/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                QuestionFeedback.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuyHouseHundredView(View):
    '''购房百科/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '购房百科':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = BuyHouseHundredDepartment.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = BuyHouseHundredDepartment.objects.all().count()
                json_dict['all_count'] = count
                a = i['classfiy_id']
                d = BuyHouseHundredDepartmentClassfiy.objects.get(id=a)
                json_dict['name'] = d.name
                json_dict['title'] = i['title']
                json_dict['classfiy_id'] = i['classfiy_id']
                json_dict['id'] = i['id']
                json_dict['two_title'] = i['two_title']
                json_dict['text_img'] = i['text_img']
                json_dict['text'] = i['text']
                json_dict['create_time'] = i['create_time']
                json_dict['click_zan'] = i['click_zan']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''购房百科/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            BuyHouseHundredDepartment.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuyHouseHundredCreateView(View):
    '''购房百科/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuyHouseHundredDepartment.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuyHouseHundredDelView(View):
    '''购房百科/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                BuyHouseHundredDepartment.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerView(View):
    '''问答/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '问答':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Question.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Question.objects.all().count()
                json_dict['all_count'] = count
                # a = i['name_id']
                # d = Question.objects.get(id=a)
                json_dict['name_id'] = i['name_id']
                json_dict['title'] = i['title']
                json_dict['id'] = i['id']
                json_dict['q_type'] = i['q_type']
                json_dict['content'] = i['content']
                json_dict['browse_count'] = i['browse_count']
                json_dict['answer_count'] = i['answer_count']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['buy_house_status'] = i['buy_house_status']
                json_dict['tou_choice'] = i['tou_choice']
                json_dict['buy_sale_choice'] = i['buy_sale_choice']
                json_dict['decoration_choice'] = i['decoration_choice']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''问答/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            Question.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerCreateView(View):
    '''问答/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Question.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerDelView(View):
    '''问答/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Question.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandDealView(View):
    '''土拍/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '土拍':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = LandAuction.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = LandAuction.objects.all().count()
                json_dict['all_count'] = count
                a = i['classfiy_name_id']
                # d = LandDistrict.objects.get(id=a)
                # json_dict['name'] = d.name
                json_dict['land_id'] = i['classfiy_name_id']
                json_dict['if_residence'] = i['if_residence']
                json_dict['if_sale'] = i['if_sale']
                json_dict['id'] = i['id']
                json_dict['land_name'] = i['land_name']
                json_dict['land_region'] = i['land_region']
                json_dict['land_position'] = i['land_position']
                json_dict['nuddle_price'] = i['nuddle_price']
                json_dict['acquisition_company'] = i['acquisition_company']
                json_dict['start_parice'] = i['start_parice']
                json_dict['end_parice'] = i['end_parice']
                json_dict['give_area'] = i['give_area']
                json_dict['deal_all_price'] = i['deal_all_price']
                json_dict['max_volume_rate'] = i['max_volume_rate']
                json_dict['overflow'] = i['overflow']
                json_dict['land_use'] = i['land_use']
                json_dict['give_year'] = i['give_year']
                json_dict['land_ask_for'] = i['land_ask_for']
                json_dict['land_number'] = i['land_number']
                json_dict['deal_date'] = i['deal_date']
                json_dict['long'] = i['long']
                json_dict['late'] = i['late']
                json_dict['land_img'] = i['land_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''土拍/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            LandAuction.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandDealCreateView(View):
    '''土拍/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            LandAuction.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandDealDelView(View):
    '''土拍/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                LandAuction.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ShareView(View):
    '''分享堂/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '分享堂':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Share.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Share.objects.all().count()
                json_dict['all_count'] = count
                a = i['middle_fk_id']
                b = i['bd_id']
                try:
                    d = MiddlePeople.objects.get(id=a)
                except Exception as e:
                    return JsonResponse({'Code': 400, 'Errmsg': str(e)})
                c = BuildingDetial.objects.get(id=b)
                json_dict['mp_name'] = d.really_name
                json_dict['building_name'] = c.building_name
                json_dict['header_img'] = d.header_img
                # json_dict['classfiy'] = i['classfiy']
                json_dict['building_fk_id'] = i['bd_id']
                json_dict['middle_fk_id'] = i['middle_fk_id']
                json_dict['create_time'] = i['create_time']
                json_dict['id'] = i['id']
                json_dict['content'] = i['content']
                json_dict['browse_count'] = i['browse_count']
                json_dict['img'] = i['img']
                json_dict['video'] = i['video']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)

    '''分享堂/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            Share.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ShareCreateView(View):
    '''分享堂/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Share.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ShareDelView(View):
    '''分享堂/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Share.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


'''系统全局设置'''


class SystemMessageSetView(View):
    '''系统消息/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '系统消息':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = SystemMessage.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = SystemMessage.objects.all().count()
                json_dict['all_count'] = count
                b = i['fk_id']
                c = BuildingDetial.objects.filter(id=b).values()
                for k in c:
                    json_dict['building_name'] = k['building_name']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''系统消息/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            SystemMessage.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SystemMessageSetCreateView(View):
    '''系统消息/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            SystemMessage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SystemMessageSetDelView(View):
    '''系统消息/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                SystemMessage.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IndexAdvertisingPKSetView(View):  # 轮播图? 需要加一个成功表
    '''首页广告竞价/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '首页广告竞价':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = GaoIndexPKMoney.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                count = GaoIndexPKMoney.objects.all().count()
                json_dict['all_count'] = count
                b = i['fk_id']
                c = MiddlePeople.objects.get(id=b)
                json_dict['really_name'] = c.really_name
                json_dict['head_img'] = c.header_img
                json_dict['price'] = i['price']
                json_dict['create_time'] = i['create_time']
                json_dict['id'] = i['id']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''首页广告竞价/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            GaoIndexPKMoney.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IndexAdvertisingPKSetCreateView(View):  # ?
    '''上楼盘之设置显示'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '上楼盘设置':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = WinPKHistory.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                b = i['fk_id']
                c = MiddlePeople.objects.get(id=b)
                json_dict['building_name'] = c.really_name
                json_dict['head_img'] = c.head_img
                json_dict['price'] = i['price']
                json_dict['create_time'] = i['create_time']
                json_dict['id'] = i['id']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''首页广告竞价/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            GaoIndexPKMoney.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IndexAdvertisingPKSetDelView(View):  # ?
    '''上楼盘之/修改广告状态'''

    def get(self, request):
        pass

    '''首页广告竞价/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                GaoIndexPKMoney.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandSetView(View):  # 添加了数据创建时间
    '''地区设置/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '地区设置':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = LandDistrict.objects.all().values()
            query = list(req)
            # paginator = Paginator(query, 10)
            # page = int(request.GET.get('page'))
            # try:
            #     page_value = paginator.page(page)
            # except EmptyPage:
            #     return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in query:
                json_dict = {}
                count = LandDistrict.objects.all().count()
                json_dict['all_count'] = count
                json_dict['name'] = i['name']
                json_dict['key_name'] = i['key_name']
                json_dict['id'] = i['id']
                # json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''地区设置/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            LandDistrict.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandSetCreateView(View):
    '''地区设置/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            LandDistrict.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandSetDelView(View):
    '''地区设置/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                LandDistrict.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SubwaySetView(View):
    '''地铁设置/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '地铁设置':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Subway.objects.all().values()
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Subway.objects.all().count()
                json_dict['all_count'] = count
                json_dict['name'] = i['name']
                json_dict['key_name'] = i['key_name']
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''地铁设置/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            Subway.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SubwaySetCreateView(View):
    '''地铁设置/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Subway.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SubwaySetDelView(View):
    '''地铁设置/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Subway.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SubwayStationSetView(View):
    '''地铁站设置/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '地铁站设置':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = SubwayStation.objects.all().values().order_by('-create_time')
            query = list(req)
            # paginator = Paginator(query, 10)
            # page = int(request.GET.get('page'))
            # try:
            #     page_value = paginator.page(page)
            # except EmptyPage:
            #     return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in query:
                json_dict = {}
                count = SubwayStation.objects.all().count()
                json_dict['all_count'] = count
                a = i['subway_id']
                b = Subway.objects.get(id=a)
                json_dict['subway_name'] = b.name
                json_dict['subway_id'] = b.id
                json_dict['name'] = i['name']
                json_dict['key_name'] = i['key_name']
                json_dict['id'] = i['id']
                # json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''地铁站设置/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            SubwayStation.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SubwayStationSetCreateView(View):
    '''地铁站设置/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            SubwayStation.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SubwayStationSetDelView(View):
    '''地铁站设置/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                SubwayStation.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BulidingChoiceClassfiySetView(View):
    '''楼盘性质类型/查'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '楼盘性质类型设置':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = BuildingClassfiy.objects.all().values()
            query = list(req)
            # paginator = Paginator(query, 10)
            # page = int(request.GET.get('page'))
            # try:
            #     page_value = paginator.page(page)
            # except EmptyPage:
            #     return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in query:
                json_dict = {}
                count = BuildingClassfiy.objects.all().count()
                json_dict['all_count'] = count
                # a = i['subway_id']
                # b = Subway.objects.get(id=a)
                # json_dict['subway_name'] = b.name
                json_dict['name'] = i['name']
                json_dict['key_name'] = i['key_name']
                json_dict['id'] = i['id']
                # json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            # total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''楼盘性质类型/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            BuildingClassfiy.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BulidingChoiceClassfiySetCreateView(View):
    '''楼盘性质类型/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingClassfiy.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BulidingChoiceClassfiySetDelView(View):
    '''楼盘性质类型/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                BuildingClassfiy.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ArticalChoiceClassfiySetView(View):
    '''文章选择类型/查(内置)'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '文章选择类型':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Article.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Article.objects.all().count()
                json_dict['all_count'] = count
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['author'] = i['author']
                json_dict['id'] = i['id']
                json_dict['author_img'] = i['author_img']
                json_dict['create_time'] = i['create_time']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['land'] = i['land']
                json_dict['new_img'] = i['new_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''文章选择类型/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            Article.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ArticalChoiceClassfiySetCreateView(View):
    '''文章选择类型/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Article.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ArticalChoiceClassfiySetDelView(View):
    '''文章选择类型/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                Article.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


'''处理'''


class CustomizeSensitiveWordSettingsView(View):
    '''自定义敏感词设置'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '自定义敏感词设置':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = SensitiveWord.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = Article.objects.all().count()
                json_dict['all_count'] = count
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['word'] = i['word']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''自定义敏感词设置/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            SensitiveWord.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CustomizeSensitiveWordSettingsCreateView(View):
    '''敏感词上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            SensitiveWord.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CustomizeSensitiveWordSettingsDelView(View):
    '''敏感词/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                SensitiveWord.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ManualMaskingOfUsersView(View):
    '''人工屏蔽用户'''

    def get(self, request):
        try:
            mp = request.GET.get('val')
            if mp != '人工屏蔽用户':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = Users.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = UserSealStatus.objects.all().count()
                json_dict['all_count'] = count
                a = i['id']
                b = UserSealStatus.objects.filter(open_id=a).values()
                for k in b:
                    json_dict['value_id'] = k['id']
                    json_dict['statue_create_time'] = k['create_time']
                    json_dict['statue'] = k['statue']
                    json_dict['choice_classfiy'] = k['choice_classfiy']
                    json_dict['if_talk'] = k['if_talk']
                json_dict['user_id'] = i['id']
                json_dict['mobile'] = i['mobile']
                json_dict['header_img'] = i['header_img']
                json_dict['really_name'] = i['really_name']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)

    '''人工屏蔽用户/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            UserSealStatus.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


'''搜索框'''


class ArticaleSearchView(View):
    '''文章搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')
            req = Article.objects.values().filter(title__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['author'] = i['author']
                json_dict['author_img'] = i['author_img']
                json_dict['create_time'] = i['create_time']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['land'] = i['land']
                json_dict['new_img'] = i['new_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''人工屏蔽用户/创建'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            UserSealStatus.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CommentSearchView(View):
    '''评论搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')
            req = Comment.objects.values().filter(title__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['catgrage_id'] = i['catgrage_id']
                json_dict['create_time'] = i['create_time']
                json_dict['click_count'] = i['click_count']
                json_dict['title'] = i['title']
                json_dict['author_name'] = i['author_name']
                json_dict['content'] = i['content']
                json_dict['head_img'] = i['head_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddleChatSearchView(View):
    '''顾问微聊搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 时间
            req = MiddlePeopleHistoryMessageRecord.objects.values().filter(create_time=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['middle_id']
                d = MiddlePeople.objects.get(id=a)
                json_dict['really_name'] = d.really_name
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserChatSearchView(View):
    '''用户微聊搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 时间
            req = UserHistoryMessageRecord.objects.values().filter(create_time=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['user_id']
                d = Users.objects.get(id=a)
                json_dict['really_name'] = d.really_name
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneHouseOnePriceSearchView(View):
    '''总一房一价搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('val')  # 预售证号
            type_id = request.GET.get('type')  # 0代表未匹配   1代表已匹配
            if int(type_id) == 0:
                # return JsonResponse({"statue": 400, 'data': 0000}, safe=False)
                total_page = OneHouseOnePrice.objects.filter(will_sale_number=mp, building_detial__isnull=True).count()
                first = OneHouseOnePrice.objects.filter(will_sale_number=mp, building_detial__isnull=True).values(
                    'lottery_title').distinct()
                first_query = list(first)
                # return JsonResponse({"statue": 400, 'data': first_query}, safe=False)
                data_list = []
                for one in first_query:
                    jd1 = {}
                    jd1['label'] = one['lottery_title']
                    # 1号楼#151#2020-11-30#商贸,写字楼#杭政储出[2017]54号#杭售许字(2020)第000134号
                    second = OneHouseOnePrice.objects.filter(lottery_title=one['lottery_title'],
                                                             building_detial__isnull=True).values('will_sale_number',
                                                                                                  'house_dong',
                                                                                                  'all_tao_count',
                                                                                                  'give_date',
                                                                                                  'house_use',
                                                                                                  'lottery_title').distinct()
                    # return JsonResponse({"statue": 400, 'data': second}, safe=False)
                    second_list = list(second)
                    # print(second_list)
                    data_list1 = []
                    for two in second_list:
                        jd2 = {}
                        thred = OneHouseOnePrice.objects.filter(will_sale_number=two['will_sale_number'],
                                                                house_dong=two['house_dong'],
                                                                building_detial__isnull=True).values('id',
                                                                                                     'door_number',
                                                                                                     'in_area',
                                                                                                     'gave_house',
                                                                                                     'one_price',
                                                                                                     'all_price',
                                                                                                     'public_date',
                                                                                                     'build_company',
                                                                                                     'create_time')
                        thred_list = list(thred)
                        jd2['house_dong'] = two['house_dong']
                        jd2['all_tao_count'] = two['all_tao_count']
                        jd2['give_date'] = two['give_date']
                        jd2['house_use'] = two['house_use']
                        jd2['lottery_title'] = two['lottery_title']
                        jd2['will_sale_number'] = two['will_sale_number']
                        jd2['children'] = thred_list
                        data_list1.append(jd2)
                    jd1['children'] = data_list1
                    data_list.append(jd1)
                if data_list == []:
                    return JsonResponse({"statue": 400, 'data': 'not_found'}, safe=False)
                return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
            else:
                # return JsonResponse({"statue": 400, 'data': 1111}, safe=False)
                total_page = OneHouseOnePrice.objects.filter(will_sale_number=mp, building_detial__isnull=False).count()
                first = OneHouseOnePrice.objects.filter(will_sale_number=mp, building_detial__isnull=False).values(
                    'lottery_title').distinct()
                first_query = list(first)
                # return JsonResponse({"statue": 400, 'data': first_query}, safe=False)
                data_list = []
                for one in first_query:
                    jd1 = {}
                    jd1['label'] = one['lottery_title']
                    # 1号楼#151#2020-11-30#商贸,写字楼#杭政储出[2017]54号#杭售许字(2020)第000134号
                    second = OneHouseOnePrice.objects.filter(lottery_title=one['lottery_title'],
                                                             building_detial__isnull=False).values('will_sale_number',
                                                                                                   'house_dong',
                                                                                                   'all_tao_count',
                                                                                                   'give_date',
                                                                                                   'house_use',
                                                                                                   'lottery_title').distinct()
                    # return JsonResponse({"statue": 400, 'data': second}, safe=False)
                    second_list = list(second)
                    # print(second_list)
                    data_list1 = []
                    for two in second_list:
                        jd2 = {}
                        thred = OneHouseOnePrice.objects.filter(will_sale_number=two['will_sale_number'],
                                                                house_dong=two['house_dong'],
                                                                building_detial__isnull=False).values('id',
                                                                                                      'door_number',
                                                                                                      'in_area',
                                                                                                      'gave_house',
                                                                                                      'one_price',
                                                                                                      'all_price',
                                                                                                      'public_date',
                                                                                                      'build_company',
                                                                                                      'create_time')
                        thred_list = list(thred)
                        jd2['house_dong'] = two['house_dong']
                        jd2['all_tao_count'] = two['all_tao_count']
                        jd2['give_date'] = two['give_date']
                        jd2['house_use'] = two['house_use']
                        jd2['lottery_title'] = two['lottery_title']
                        jd2['will_sale_number'] = two['will_sale_number']
                        jd2['children'] = thred_list
                        data_list1.append(jd2)
                    jd1['children'] = data_list1
                    data_list.append(jd1)
                if data_list == []:
                    return JsonResponse({"statue": 400, 'data': 'not_found'}, safe=False)
                return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''一房一价筛选查询'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            # cd = json_dict.get('house_dong__in')
            page = json_dict.get('page')
            del json_dict['page']
            req = OneHouseOnePrice.objects.values().filter(**json_dict).order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(page)
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['building_detial_id']
                d = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = d.building_name
                json_dict['house_dong'] = i['house_dong']
                json_dict['house_yuan'] = i['house_yuan']
                json_dict['house_ceng'] = i['house_ceng']
                json_dict['door_number'] = i['door_number']
                json_dict['if_sale'] = i['if_sale']
                json_dict['classfiy'] = i['classfiy']
                json_dict['decorate_type'] = i['decorate_type']
                json_dict['decorate_type_price'] = i['decorate_type_price']
                json_dict['area'] = i['area']
                json_dict['house_xing'] = i['house_xing']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                # json_dict['result'] = i['result']
                json_dict['gave_house'] = i['gave_house']
                json_dict['lottery_ci'] = i['lottery_ci']
                json_dict['water_money'] = i['water_money']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LotterySearchView(View):
    '''摇号搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('val')  # 楼盘名称
            req = HistoryLottery.objects.values().filter(detial__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['lottery_time'] = i['lottery_time']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['decorate_situation'] = i['decorate_situation']
                json_dict['house'] = i['house']
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['house_count'] = i['house_count']
                json_dict['people_count'] = i['people_count']
                json_dict['win_probability'] = i['win_probability']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LandSearchView(View):
    '''土拍搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 地区名称
            req = LandAuction.objects.values().filter(classfiy_name__name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['if_residence'] = i['if_residence']
                json_dict['if_sale'] = i['if_sale']
                json_dict['land_name'] = i['land_name']
                json_dict['land_region'] = i['land_region']
                json_dict['land_position'] = i['land_position']
                json_dict['nuddle_price'] = i['nuddle_price']
                json_dict['acquisition_company'] = i['acquisition_company']
                json_dict['end_parice'] = i['end_parice']
                json_dict['give_area'] = i['give_area']
                json_dict['deal_all_price'] = i['deal_all_price']
                json_dict['max_volume_rate'] = i['max_volume_rate']
                json_dict['overflow'] = i['overflow']
                json_dict['land_use'] = i['land_use']
                json_dict['give_year'] = i['give_year']
                json_dict['land_ask_for'] = i['land_ask_for']
                json_dict['land_number'] = i['land_number']
                json_dict['for_remark'] = i['for_remark']
                json_dict['long'] = i['long']
                json_dict['late'] = i['late']
                json_dict['deal_date'] = i['deal_date']
                json_dict['land_img'] = i['land_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerSearchView(View):
    '''问答搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 问答标题
            req = Question.objects.values().filter(title__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['author'] = i['author']
                json_dict['q_type'] = i['q_type']
                json_dict['create_time'] = i['create_time']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['browse_count'] = i['browse_count']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['buy_house_status'] = i['buy_house_status']
                json_dict['tou_choice'] = i['tou_choice']
                json_dict['buy_sale_choice'] = i['buy_sale_choice']
                json_dict['decoration_choice'] = i['decoration_choice']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ShareSearchView(View):
    '''分享堂搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 楼盘名称
            req = Share.objects.values().filter(building_fk__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['middle_fk_id']
                d = MiddlePeople.objects.get(id=a)
                c = i['building_fk_id']
                b = BuildingDetial.objects.get(id=c)
                json_dict['mp_name'] = d.really_name
                json_dict['mp_name'] = b.building_name
                json_dict['classfiy'] = i['classfiy']
                json_dict['building_name'] = i['building_name']
                json_dict['author'] = i['author']
                json_dict['create_time'] = i['create_time']
                json_dict['content'] = i['content']
                json_dict['browse_count'] = i['browse_count']
                json_dict['img'] = i['img']
                json_dict['video'] = i['video']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['head_img'] = i['head_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddlePeopleClickSearchView(View):
    '''顾问点赞记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 楼盘名称
            req = Share.objects.values().filter(building_fk__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['middle_fk_id']
                d = MiddlePeople.objects.get(id=a)
                c = i['building_fk_id']
                b = BuildingDetial.objects.get(id=c)
                json_dict['mp_name'] = d.really_name
                json_dict['mp_name'] = b.building_name
                json_dict['classfiy'] = i['classfiy']
                json_dict['building_name'] = i['building_name']
                json_dict['author'] = i['author']
                json_dict['create_time'] = i['create_time']
                json_dict['content'] = i['content']
                json_dict['land'] = i['land']
                json_dict['browse_count'] = i['browse_count']
                json_dict['img'] = i['img']
                json_dict['video'] = i['video']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['head_img'] = i['head_img']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


'''----------------------------------'''


# class MiddlePeopleLTSearchView(View):
#     '''顾问聊天记录搜索框'''
#     def get(self, request):
#         try:
#             mp = request.GET.get('asv') # 顾问名称
#             req = MiddlePeopleHistoryMessageRecord.objects.values().filter(fk__really_name__contains=mp)
#             query = list(req)
#             paginator = Paginator(query, 10)
#             page = int(request.GET.get('page'))
#             try:
#                 page_value = paginator.page(page)
#             except EmptyPage:
#                 return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
#             data_list = []
#             for i in page_value:
#                 json_dict = {}
#                 json_dict['id'] = i['id']
#                 a = i['middle_fk_id']
#                 d = MiddlePeople.objects.get(id=a)
#                 json_dict['mp_name'] = d.really_name
#                 json_dict['user_id'] = i['user_id']
#                 json_dict['middle_id'] = i['middle_id']
#                 json_dict['content'] = i['content']
#                 json_dict['create_time'] = i['create_time']
#                 data_list.append(json_dict)
#             total_page = paginator.num_pages
#             return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
#         except Exception as e:
#             context = {"Result": 'false', 'Msg': {e}}
#             return JsonResponse(context)


class MiddlePeopleFWSearchView(View):
    '''顾问访客记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = MiddlePeople.objects.values('id', 'really_name').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                b = i['id']
                date = WhoLookMiddelPeople.objects.get(fk_id=b)
                json_dict['id'] = date.id
                json_dict['really_name'] = i['really_name']
                json_dict['name'] = date.create_time
                json_dict['user_id'] = date.user_id
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ComePhoneSearchView(View):
    '''来电记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            # mp1 = request.GET.get('mp_id')
            req = MiddlePeople.objects.values('id', 'really_name').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                b = i['id']
                date = MyPhoneCall.objects.get(middle_people_id=b)
                json_dict['id'] = date.id
                json_dict['really_name'] = i['really_name']
                json_dict['name'] = date.name
                json_dict['user_id'] = date.user_id
                json_dict['phone_time'] = date.phone_time
                json_dict['user_phone'] = date.user_phone
                json_dict['create_time'] = date.create_time
                json_dict['head_img'] = date.head_img
                json_dict['choice_classfiy'] = date.choice_classfiy
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CatagtleCustmersSearchView(View):
    '''专属客户搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = MiddlePeople.objects.values('id', 'really_name').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                b = i['id']
                date = ExclusiveCustmer.objects.get(middle_name_id=b)
                json_dict['id'] = date.id
                json_dict['really_name'] = i['really_name']
                json_dict['user_id'] = date.user_id
                json_dict['user_id'] = date.user_name
                json_dict['user_id'] = date.custmer_time
                json_dict['head_img'] = date.head_img
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class GiveCGODBotSearchView(View):
    '''获客神器搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = MiddlePeople.objects.values('id', 'really_name').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                b = i['id']
                date = ReallyNameMiddlePeopleShare.objects.get(fk_id=b)
                json_dict['id'] = date.id
                json_dict['really_name'] = i['really_name']
                json_dict['user_id'] = date.user_id
                json_dict['middle_id'] = date.middle_id
                json_dict['name'] = date.name
                json_dict['create_time'] = date.create_time
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MoneyChangeSearchView(View):
    '''金币记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = MiddlePeople.objects.values('id', 'really_name').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                b = i['id']
                date = GoldenMoney.objects.get(fk_id=b)
                json_dict['id'] = date.id
                json_dict['really_name'] = i['really_name']
                json_dict['money_count'] = date.money_count
                json_dict['recharge_time'] = date.recharge_time
                json_dict['change_beacuse'] = date.change_beacuse
                json_dict['create_time'] = date.create_time
                json_dict['choice_classfiy'] = date.choice_classfiy
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


# class HouseBuildingSearchView(View):
#     '''入住楼盘搜索框'''
#     def get(self, request):
#         try:
#             mp = request.GET.get('user_name')  # 用户名称
#             req = Users.objects.values('id').filter(really_name__contains=mp)
#             query = list(req)
#             paginator = Paginator(query, 10)
#             page = int(request.GET.get('page'))
#             try:
#                 page_value = paginator.page(page)
#             except EmptyPage:
#                 return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
#             data_list = []
#             for i in page_value:
#                 json_dict = {}
#                 json_dict['id'] = i['id']
#                 a = i['id']
#                 d = AttentionMiddlePeopleVillage.objects.get(user_id=a)
#                 date = Article.objects.get(id=b)
#                 json_dict['id'] = date.id
#                 json_dict['land'] = date.land_id
#                 json_dict['choice_classfiy'] = date.choice_classfiy
#                 json_dict['author'] = date.author
#                 json_dict['author_img'] = date.author_img
#                 json_dict['create_time'] = date.create_time
#                 json_dict['title'] = date.title
#                 json_dict['content'] = date.content
#                 json_dict['land'] = date.land
#                 json_dict['new_img'] = date.new_img
#                 data_list.append(json_dict)
#             total_page = paginator.num_pages
#             return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
#         except Exception as e:
#             context = {"Result": 'false', 'Msg': {e}}
#             return JsonResponse(context)


# class RankSearchView(View): # ?这个不需要搜索吧
#     '''顾问等级搜索框'''
#     def get(self, request):
#         try:
#             mp = request.GET.get('asv') # 楼盘名称
#             req = Share.objects.values().filter(building_fk__building_name__contains=mp)
#             query = list(req)
#             paginator = Paginator(query, 10)
#             page = int(request.GET.get('page'))
#             try:
#                 page_value = paginator.page(page)
#             except EmptyPage:
#                 return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
#             data_list = []
#             for i in page_value:
#                 json_dict = {}
#                 json_dict['id'] = i['id']
#                 a = i['middle_fk_id']
#                 d = MiddlePeople.objects.get(id=a)
#                 c = i['building_fk_id']
#                 b = BuildingDetial.objects.get(id=c)
#                 json_dict['mp_name'] = d.really_name
#                 json_dict['mp_name'] = b.building_name
#                 json_dict['classfiy'] = i['classfiy']
#                 json_dict['building_name'] = i['building_name']
#                 json_dict['author'] = i['author']
#                 json_dict['create_time'] = i['create_time']
#                 json_dict['content'] = i['content']
#                 json_dict['land'] = i['land']
#                 json_dict['browse_count'] = i['browse_count']
#                 json_dict['img'] = i['img']
#                 json_dict['video'] = i['video']
#                 json_dict['choice_classfiy'] = i['choice_classfiy']
#                 json_dict['head_img'] = i['head_img']
#                 data_list.append(json_dict)
#             total_page = paginator.num_pages
#             return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
#         except Exception as e:
#             context = {"Result": 'false', 'Msg': {e}}
#             return JsonResponse(context)


class LoginSearchView(View):
    '''登陆记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = Users.objects.values('id').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['id']
                try:
                    d = Users.objects.get(id=a)
                    json_dict['name'] = d.really_name
                    date = UserLoginRecord.objects.get(fk_id=a)
                    json_dict['id'] = date.id
                    json_dict['user_name'] = date.user_name
                    json_dict['header_img'] = date.header_img
                    json_dict['mobile'] = date.mobile
                    data_list.append(json_dict)
                except:
                    context = {"Result": 'false', 'Msg': []}
                    return JsonResponse(context)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionBuildingSearchView(View):
    '''访问楼盘记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = Users.objects.values('id').filter(really_name__contains=mp)
            # req = Users.objects.values('id').filter(really_name=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['id']
                d = Users.objects.get(id=a)
                json_dict['name'] = d.really_name
                date = UserLoginBuildingRecord.objects.get(fk_id=a)
                json_dict['id'] = date.id
                json_dict['user_name'] = date.user_name
                json_dict['header_img'] = date.header_img
                json_dict['mobile'] = date.mobile
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AllChatMiddlePeopleSearchView(View):
    '''总聊天记录搜索框/顾问'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 顾问说的话
            req = MiddlePeopleHistoryMessageRecord.objects.values().filter(content__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['fk_id']
                d = MiddlePeople.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AllChatUsersSearchView(View):
    '''总聊天记录搜索框/用户'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 用户说的话
            req = UserHistoryMessageRecord.objects.values().filter(content__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['fk_id']
                d = Users.objects.get(id=a)
                json_dict['user_name'] = d.really_name
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LotteryNumberValueSearchView(View):
    '''摇号数据搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 楼盘名称
            req = UserLotteryNumber.objects.values().filter(build_id__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['user_id_id']
                d = Users.objects.get(id=a)
                c = i['building_fk_id']
                b = BuildingDetial.objects.get(id=c)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['mp_name'] = b.building_name
                json_dict['create_time'] = i['create_time']
                json_dict['number'] = i['number']
                json_dict['really_name'] = i['really_name']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserAttertionArticalSearchView(View):
    '''用户关注的文章搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = Users.objects.values('id').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['id']
                d = AttentionAretical.objects.get(user_id=a)
                b = d.aretical_id
                date = Article.objects.get(id=b)
                json_dict['id'] = date.id
                json_dict['land'] = date.land_id
                json_dict['choice_classfiy'] = date.choice_classfiy
                json_dict['author'] = date.author
                json_dict['author_img'] = date.author_img
                json_dict['create_time'] = date.create_time
                json_dict['title'] = date.title
                json_dict['content'] = date.content
                json_dict['land'] = date.land
                json_dict['new_img'] = date.new_img
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserAttertionBuildingSearchView(View):
    '''用户关注的楼盘搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = Users.objects.values('id').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['id']
                d = AttentionVillage.objects.get(user_id=a)
                b = d.building_id
                date = BuildingDetial.objects.get(id=b)
                json_dict['id'] = date.id
                json_dict['land'] = date.land_id
                json_dict['train'] = date.train_id
                json_dict['budling_other'] = date.budling_other_id
                json_dict['building_name'] = date.building_name
                json_dict['unit_price'] = date.unit_price
                json_dict['sale_stage_time'] = date.sale_stage_time
                json_dict['sale_building_location'] = date.sale_building_location
                json_dict['longitude'] = date.longitude
                json_dict['latitude'] = date.latitude
                json_dict['if_index_advertising'] = date.if_index_advertising
                json_dict['if_lunbo_choice'] = date.if_lunbo_choice
                json_dict['if_building_detail_advertising'] = date.if_building_detail_advertising
                json_dict['attention_degree'] = date.attention_degree
                json_dict['comment_count'] = date.comment_count
                json_dict['bussiness_building'] = date.bussiness_building
                json_dict['open_house_number'] = date.open_house_number
                json_dict['will_sale_number'] = date.will_sale_number
                json_dict['create_time'] = date.create_time
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserAttertionMiddlePeopleSearchView(View):
    '''用户关注的置业顾问搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('user_name')  # 用户名称
            req = Users.objects.values('id').filter(really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                # json_dict['id'] = i['id']
                a = i['id']
                d = AttentionMiddlePeople.objects.get(user_id=a)
                b = d.middle_people_id
                date = MiddlePeople.objects.get(id=b)
                json_dict['nick_name'] = date.nick_name
                json_dict['mobile'] = date.mobile
                json_dict['id'] = date.id
                json_dict['header_img'] = date.header_img
                json_dict['personal_introduce'] = date.personal_introduce
                json_dict['really_name'] = date.really_name
                json_dict['ID_card'] = date.ID_card
                json_dict['give_price_history'] = date.give_price_history
                json_dict['invitation_code'] = date.invitation_code
                json_dict['two_wei_ma'] = date.two_wei_ma
                json_dict['work_pai'] = date.work_pai
                json_dict['golden_money'] = date.golden_money
                json_dict['integral'] = date.integral
                json_dict['click_count'] = date.click_count
                json_dict['live_limit'] = date.live_limit
                json_dict['browse_count'] = date.browse_count
                json_dict['bussiness_building'] = date.bussiness_building
                json_dict['rank'] = date.rank
                json_dict['create_time'] = date.create_time
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserLotterySearchView(View):
    '''用户摇号搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 楼盘名称
            req = UserLotteryNumber.objects.values().filter(build_id__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['user_id_id']
                d = Users.objects.get(id=a)
                c = i['build_id_id']
                b = BuildingDetial.objects.get(id=c)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['mp_name'] = b.building_name
                json_dict['number'] = i['number']
                json_dict['create_time'] = i['create_time']
                json_dict['really_name'] = i['really_name']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserCodeSearchView(View):
    '''用户编码搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 楼盘名称
            req = UserCodeNumber.objects.values().filter(build_id__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['user_id_id']
                d = Users.objects.get(id=a)
                c = i['build_id_id']
                b = BuildingDetial.objects.get(id=c)
                json_dict['user_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['mp_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['really_name'] = i['really_name']
                json_dict['create_time'] = i['create_time']
                json_dict['number'] = i['number']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserScoresSearchView(View):
    '''顾问积分记录搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # because
            req = IntegralSubsidiary.objects.values().filter(change_beacuse__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['fk_id']
                json_dict['score'] = i['score']
                json_dict['id'] = i['id']
                json_dict['score_create_time'] = i['score_create_time']
                json_dict['change_beacuse'] = i['change_beacuse']
                json_dict['create_time'] = i['create_time']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


#  ----------------------------------


class SysteamMessageSearchView(View):
    '''系统消息搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 楼盘名称
            req = SystemMessage.objects.values().filter(fk__building_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['fk_id']
                d = BuildingDetial.objects.get(id=a)
                json_dict['mp_name'] = d.building_name
                json_dict['title'] = i['title']
                json_dict['bd_id'] = i['bd_id']
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IndexPkGaoMoneySearchView(View):
    '''首页广告竞价搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 顾问名
            req = WinPKHistory.objects.values().filter(fk__really_name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                a = i['fk_id']
                d = MiddlePeople.objects.get(id=a)
                json_dict['mp_name'] = d.really_name
                json_dict['header_img'] = d.header_img
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['id'] = i['id']
                json_dict['building_id'] = i['building_id']
                json_dict['price'] = i['price']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''微聊/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            classfiy = json_dict.get('classfiy')
            bd = json_dict.get('id')
            del json_dict['classfiy']
            if classfiy == '顾问':
                for i in bd:
                    MiddlePeopleHistoryMessageRecord.objects.filter(id=i).delete()
            elif classfiy == '用户':
                for i in bd:
                    UserHistoryMessageRecord.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


# 修改的是换绑楼盘
class LandDistarnSearchView(View):
    '''地区搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 用户名
            req = LandDistrict.objects.values().filter(name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['name'] = i['name']
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''意向登记未匹配/修改'''

    def post(self, request):
        try:
            # start 开始修改
            # 获取的是列表UnionLotteryResult的要更换的id
            id = request.POST.get("id")
            new_union = UnionLotteryResult.objects.get(id=id)
            # 获取的是列表UnionLotteryResult的已绑定的id
            union_id = request.POST.get("union_id")
            old_union = UnionLotteryResult.objects.get(id=union_id)
            if not (new_union and old_union):
                return JsonResponse({"statue": 200, 'data': []}, safe=False)
            # 需要把ToldPurpose中的fk_id 改成 新的fk_id
            toldPurposes = ToldPurpose.objects.filter(fk_id=old_union.fk_id).values()
            toldPurposeList = list(toldPurposes)
            # return JsonResponse({"statue": 200, 'data': toldPurposeList}, safe=False)
            for i in toldPurposeList:
                ToldPurpose.objects.filter(id=i['id']).update(fk_id=new_union.fk_id)
            # end 修改结束
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class TrainSearchView(View):
    '''地铁搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 用户名
            req = Subway.objects.values().filter(name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['name'] = i['name']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''摇号未匹配/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            del json_dict['id']
            LotteryResult.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class TrainStationSearchView(View):
    '''地铁站搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv')  # 用户名
            req = SubwayStation.objects.values().filter(name__contains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['subway_id']
                d = Subway.objects.get(id=a)
                json_dict['subway'] = d.name
                json_dict['header_img'] = d.header_img
                json_dict['name'] = i['name']
                json_dict['id'] = i['id']
                json_dict['subway_id'] = i['subway_id']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''总微聊顾问/用户评论记录'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('asv')
            pg = json_dict.get('page')
            del json_dict['asv']
            del json_dict['page']
            if bd == '总微聊顾问':
                req = MiddlePeopleHistoryMessageRecord.objects.all().values()
                query = list(req)
                paginator = Paginator(query, 10)
                page = int(pg)
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['fk_id']
                    b = Users.objects.get(id=a)
                    c = i['user_bei_id']
                    d = Users.objects.get(id=c)
                    json_dict['user_name'] = b.really_name
                    json_dict['middle_name'] = d.really_name
                    json_dict['id'] = i['id']
                    json_dict['user_id'] = i['fk_id']
                    json_dict['middle_id'] = i['user_bei_id']
                    json_dict['content'] = i['content']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                total_page = paginator.num_pages
                return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
            elif bd == '总微聊用户':
                req = UserHistoryMessageRecord.objects.all().values()
                query = list(req)
                paginator = Paginator(query, 10)
                page = int(pg)
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                data_list = []
                for i in page_value:
                    json_dict = {}
                    aa = i['fk_id']
                    bb = Users.objects.get(id=aa)
                    ca = i['user_bei_id']
                    da = Users.objects.get(id=ca)
                    json_dict['user_name'] = bb.really_name
                    json_dict['middle_name'] = da.really_name
                    json_dict['id'] = i['id']
                    json_dict['user_id'] = i['fk_id']
                    json_dict['middle_id'] = i['user_bei_id']
                    json_dict['content'] = i['content']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                total_page = paginator.num_pages
                return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
            else:
                context = {"Result": 'false', 'Msg': 'value_false'}
                return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)


class BuyHoseBaiKeSearchView(View):
    '''购房百科搜索框'''

    def get(self, request):
        try:
            mp = request.GET.get('asv') or ''  # 标题
            req = BuyHouseHundredDepartment.objects.values().filter(title__icontains=mp)
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page') or 1)
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['classfiy'] = i['classfiy_id']
                json_dict['title'] = i['title']
                json_dict['two_title'] = i['two_title']
                json_dict['text_img'] = i['text_img']
                json_dict['text'] = i['text']
                json_dict['create_time'] = i['create_time']
                json_dict['click_zan'] = i['click_zan']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)

    '''总评论'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('asv')
            pg = json_dict.get('page')
            del json_dict['asv']
            del json_dict['page']
            if bd == '总评论数据':
                req = Comment.objects.filter(catgrage_id__isnull=True).values()
                query = list(req)
                paginator = Paginator(query, 10)
                page = int(pg)
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['id']
                    req2 = Comment.objects.filter(catgrage_id=a).values()
                    reqlist = list(req2)
                    json_dict['create_time'] = i['create_time']
                    json_dict['click_count'] = i['click_count']
                    json_dict['author_name'] = i['author_name']
                    json_dict['author_id'] = i['author_id']
                    json_dict['village_id'] = i['village_id']
                    c = i['village_id']
                    b = BuildingDetial.objects.get(id=c)
                    json_dict['building_name'] = b.building_name
                    json_dict['title'] = i['title']
                    json_dict['content'] = i['content']
                    json_dict['head_img'] = i['head_img']
                    json_dict['dian_ping'] = reqlist
                    data_list.append(json_dict)
                total_page = paginator.num_pages
                return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
            else:
                context = {"Result": 'false', 'Msg': 'value_false'}
                return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)


class AllBuildingDetialSearchView(View):
    '''总楼盘销售时间搜索框'''

    def get(self, request):
        try:
            bd = request.GET.get('val')  # 楼盘名称
            req1 = BuildingDetial.objects.filter(building_name__contains=bd).values('id')
            req2 = list(req1)
            b = []
            for ii in req2:
                a = ii['id']
                b.append(a)
            req = BuildingStatueTimeSale.objects.filter(fk_id__in=b).values()
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = BuildingStatueTimeSale.objects.all().count()
                json_dict['all_count'] = count
                a = i['fk_id']
                b = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['will_sale_time'] = i['will_sale_time']
                json_dict['register_time'] = i['register_time']
                json_dict['commit_time'] = i['commit_time']
                json_dict['want_told_time'] = i['want_told_time']
                json_dict['lottery_time'] = i['lottery_time']
                json_dict['choice_house_time'] = i['choice_house_time']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialPkMoneySearchView(View):
    '''楼盘详情页竞价搜索框'''

    def get(self, request):  # 分类查询
        try:
            bd = request.GET.get('val')  # 楼盘名称
            req1 = MiddlePeople.objects.filter(really_name__contains=bd).values('id')
            req2 = list(req1)
            b = []
            for ii in req2:
                a = ii['id']
                b.append(a)
            req = GaoBuildingDetialPKMoney.objects.filter(fk_id__in=b).values()
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = GaoBuildingDetialPKMoney.objects.filter(building_id=bd).count()
                json_dict['all_count'] = count
                a = i['building_id']
                b = BuildingDetial.objects.get(id=a)
                aa = i['fk_id']
                bb = MiddlePeople.objects.get(id=aa)
                json_dict['middle_name'] = bb.really_name
                json_dict['building_name'] = b.building_name
                json_dict['id'] = i['id']
                json_dict['price'] = i['price']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SensitiveWordDepartView(View):
    '''用户禁言接口'''

    def get(self, request):
        try:
            mp = request.GET.get('user_id')  # 顾问名称
            req = UserSealStatus.objects.get(fk_id=mp)
            json_dict = {}
            data_list = []
            json_dict['fk_id'] = req.fk
            json_dict['create_time'] = req.create_time
            json_dict['statue'] = req.statue
            json_dict['choice_classfiy'] = req.choice_classfiy
            json_dict['if_talk'] = req.if_talk
            data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''敏感词查询'''

    def post(self, request):
        try:
            bd = request.POST.get('val')  # 接收传入的字符串
            cd = request.POST.get('statue')  # 状态
            req = SensitiveWord.objects.filter(choice_classfiy=cd).values()
            data_list = list(req)
            req_list = []
            for i in data_list:
                ii = i['word']
                if ii in bd:
                    js = {}
                    new_str = bd.replace(ii, '**')
                    js['word'] = ii
                    js['data'] = new_str
                    req_list.append(js)
            return JsonResponse({"statue": 200, 'data': req_list, 'MSG': '包含敏感词'}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CustomMaskingView(View):
    '''自定义聊天屏蔽/查改'''  # MaxConnectionAndMaxPeopleAndMaxCountView

    def get(self, request):  # 分类查询
        try:
            # mp = request.GET.get('val_id')  # 1 为 评论的, 2 为 微聊的
            req = MaxConnectionAndMaxPeopleAndMaxCountView.objects.filter().values()
            query = list(req)
            data_list = []
            for i in query:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['chat_second'] = i['chat_second']
                json_dict['chat_people'] = i['chat_people']
                json_dict['chat_count'] = i['chat_count']
                data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''自定义聊天屏蔽/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            MaxConnectionAndMaxPeopleAndMaxCountView.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CustomMaskingCreateView(View):
    '''自定义聊天屏蔽/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            MaxConnectionAndMaxPeopleAndMaxCountView.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CustomMaskingDelView(View):
    '''自定义聊天屏蔽/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                MaxConnectionAndMaxPeopleAndMaxCountView.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MicrochatFrequencyLimitView(View):
    '''微聊频率限制'''
    pass


class ThePriestClimbsTenWhileTheDevilClimbsTenView(View):
    '''反抓取屏蔽'''
    pass


class UploadBuildingFindYXDJView(View):
    '''上传楼盘时关联意向登记'''

    def get(self, request):  # 筛选
        try:
            mp = request.GET.get('building_name')
            req = UnionLotteryResult.objects.filter(building_name__contains=mp).values()
            co = UnionLotteryResult.objects.filter(building_name__contains=mp).count()
            try:
                query = list(req)[0]
            except:
                return JsonResponse({"statue": 200, 'data': '无可用意向登记'}, safe=False)
            data_list = []
            json_dict = {}
            json_dict['id'] = query['id']
            json_dict['pid'] = query['pid']
            # json_dict['fk_id'] = query['fk_id']
            json_dict['building_name'] = query['building_name']
            json_dict['count'] = co
            data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list, 'msg': '匹配到意向登记, 是否关联?'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    # 修改意向登记关联
    def post(self, request):
        try:
            pd = request.POST.get('pid')
            fk = request.POST.get('fk_id')
            UnionLotteryResult.objects.filter(pid=pd).update(fk_id=fk)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UploadBuildingFindYFYJView(View):
    '''上传楼盘时关联一房一价'''

    def get(self, request):
        try:
            mp = request.GET.get('will_sale_number')
            req = OneHouseOnePrice.objects.filter(will_sale_number=mp).values()
            co = OneHouseOnePrice.objects.filter(will_sale_number=mp).count()
            try:
                query = list(req)[0]
            except:
                return JsonResponse({"statue": 200, 'data': '无可用一房一价'}, safe=False)
            data_list = []
            json_dict = {}
            json_dict['id'] = query['id']
            json_dict['will_sale_number'] = query['will_sale_number']
            json_dict['building_detial_id'] = query['building_detial_id']
            # json_dict['building_name'] = query['building_name']
            json_dict['count'] = co
            data_list.append(json_dict)
            return JsonResponse({"statue": 200, 'data': data_list, 'msg': '匹配到一房一价, 是否关联?'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    # 修改一房一价关联
    def post(self, request):
        try:
            pd = request.POST.get('bd_id')
            fk = request.POST.get('will_sale_number')
            OneHouseOnePrice.objects.filter(will_sale_number=fk).update(building_detial_id=pd)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MessageTemplateView(View):
    '''消息模板/查'''

    def get(self, request):
        try:
            mp = request.GET.get('pfv')
            if mp != '消息模板':
                return JsonResponse({"statue": 400, 'data': 'value_fale'}, safe=False)
            req = MessageTemplateValue.objects.all().values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = MessageTemplateValue.objects.all().count()
                json_dict['template_all_count'] = count
                json_dict['id'] = i['id']
                json_dict['template_id'] = i['template_id']
                json_dict['template_name'] = i['template_name']
                json_dict['template_recode'] = i['template_recode']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''消息模板/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            MessageTemplateValue.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MessageTemplateCreateView(View):
    '''模板消息/搜索'''

    def get(self, request):
        try:
            mp = request.GET.get('search')
            req = MessageTemplateValue.objects.filter(template_name__contains=mp).values().order_by('-create_time')
            query = list(req)
            paginator = Paginator(query, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            data_list = []
            for i in page_value:
                json_dict = {}
                count = MessageTemplateValue.objects.all().count()
                json_dict['template_all_count'] = count
                json_dict['id'] = i['id']
                json_dict['template_id'] = i['template_id']
                json_dict['template_name'] = i['template_name']
                json_dict['template_recode'] = i['template_recode']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            total_page = paginator.num_pages
            return JsonResponse({"statue": 200, 'data': data_list, 'count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''消息模板/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            MessageTemplateValue.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MessageTemplateDelView(View):
    '''消息模板/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                MessageTemplateValue.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

        # 添加获取所有楼盘


class BuildingDetailDoneView(View):
    '''获取楼盘列表'''

    def get(self, request):
        try:
            detail_data = BuildingDetial.objects.values()
            detail_list = list(detail_data)
            data_list = []
            for i in detail_list:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['building_name'] = i['building_name']
                data_list.append(json_dict)
            if detail_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''绑定楼盘'''

    def post(self, request):
        try:
            # start 开始修改
            id = request.POST.get('id')  # 意向登记和摇号结果的联合id
            fk_id = request.POST.get('fk_id')  # building_detail的主键id
            result = UnionLotteryResult.objects.get(id=id)
            result.fk_id = fk_id
            result.save()
            # end   结束修改
            return JsonResponse({"statue": 200, 'data': '更新成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)
