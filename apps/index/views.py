import json
from django.db.models import Q, F
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.views import View

from authorization.models import MiddlePeople, Users, AttentionVillage, IntegralSubsidiary, MiddleUnionId, \
    UserLoginBuildingRecord
from index.models import OtherImg, BuildingDetial, LandDistrict, BuildingImage, IssueBuildingDynamicMessage, \
    SubwayStation, \
    PublicPlan, BuildingStatueTimeSale, ToldPurpose, OneHouseOnePrice, QuestionEveryProblem, BuyHouseHundredDepartment, \
    BuyHouseHundredDepartmentClassfiy, HistoryLottery, Article, LandAuction, Share, Subway, Question, Answer, \
    UserAnswerBuilding, HouseImage, BuildingVideo, Comment, ZanCount, VRAerialPhotoAllPingImage, \
    BuildingOneHouseOnePriceImage, UnionLotteryResult, LotteryResult
from utils.auth import already_authorized, get_user, kanfanghuifuxiaoxituisong, yaohaojieguotongzhi
from utils.map import getlnglat, surrounding_facility

import datetime


class HomePageView(View):
    def get(self, request):
        return HttpResponse('..此乃首页..')


class SearchView(View):
    '''首页/找房-搜索框'''

    def get(self, request):
        try:
            data = request.GET.get('value')
            query_data = BuildingDetial.objects.values().filter(building_name__icontains=data)
            query_list = list(query_data)
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']
                json_dict['only_id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['comment_count'] = i['comment_count']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['train_id'] = i['train_id']
                json_dict['unit_price'] = i['unit_price']
                json_dict['fly'] = None  # 暂无

                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa

                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)

    def post(self, request):
        try:
            if request.POST.get('sing') == 'yes':
                query_data = BuildingDetial.objects.values().all()
                query_list = list(query_data)
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['building_name'] = i['building_name']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class WheelImageView(View):
    '''轮播图1/轮播图2'''

    def get(self, request):
        try:
            query_data = BuildingDetial.objects.filter(if_index_advertising='1').values('id')
            query_list = list(query_data)
            data_list = []
            for i in query_list[:4]:
                i_d = i['id']
                d = BuildingImage.objects.values().filter(fk_id=i_d)
                d_l = list(d)
                json_dict = {}
                for a in d_l:
                    json_dict['photo_image'] = a['photo_image']
                json_dict['id'] = i_d
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    def post(self, request):
        try:
            query_data = BuildingDetial.objects.all().values('id', 'building_name').order_by('-create_time')
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['bd_id'] = i['id']
                json_dict['building_name'] = i['building_name']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HeadersNuddleView(View):
    '''头条'''

    def get(self, request):
        try:
            data = request.GET.get('header_tiao')  # 头条
            if data == '头条':
                query_data = Article.objects.values().all().order_by('-create_time')
                query_list = list(query_data)
                data_list = []
                for i in query_list:
                    json_dict = {}
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['title'] = i['title']
                    json_dict['content'] = i['content']
                    json_dict['new_img'] = i['new_img']
                    json_dict['author_img'] = i['author_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
            else:
                return JsonResponse({'Code': 400,
                                     'Errmsg': '参数错误'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HotDoorBuildingView(View):
    '''热门楼盘: 热门榜/人气榜/访问帮/热评榜(热门推荐)'''

    def get(self, request):

        if request.GET.get('notice') == '热门':
            try:
                # query_data = BuildingDetial.objects.values().all().order_by('-attention_degree', '-comment_count')
                query_data = BuildingDetial.objects.values().order_by('create_time')
                # query_data = BuildingDetial.objects.filter(sale_stage='热门楼盘').values()
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    # json_dict['land_id'] = i['train_traffic']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    json_dict['only_id'] = i['id']

                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa

                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('notice') == '人气':
            # people_count
            try:
                # query_data = BuildingDetial.objects.values().all().order_by('-attention_degree', '-comment_count')
                query_data = BuildingDetial.objects.values().order_by('-total_price')
                # query_data = BuildingDetial.objects.filter(sale_stage='热门楼盘').values()
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    # json_dict['land_id'] = i['train_traffic']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    json_dict['only_id'] = i['id']

                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa

                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': str(e)}
                return JsonResponse(context)

        elif request.GET.get('notice') == '评论':
            try:
                query_data = BuildingDetial.objects.values().order_by('-comment_count')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('notice') == '访问':
            try:
                query_data = BuildingDetial.objects.values().order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)


class IndexCountView(View):
    '''统计五个组件'''

    def get(self, request):
        try:
            # sale_stage 即将预售/正在公示/正在登记/最新摇号/无需摇号(不限购)/已摇号/等待摇号
            rm = BuildingDetial.objects.filter(sale_stage__contains='热门楼盘').count()
            ws = BuildingDetial.objects.filter(sale_stage__contains='即将预售').count()
            wt = BuildingDetial.objects.filter(sale_stage__contains='即将摇号').count()
            gt = BuildingDetial.objects.filter(sale_stage__contains='摇号剩余').count()
            nl = BuildingDetial.objects.filter(sale_stage__contains='热门楼盘').count()

            data_list = []
            json_dict = {}
            json_dict['hot_build'] = rm
            json_dict['wile_sale'] = ws
            json_dict['go_told'] = wt
            json_dict['go_write'] = gt
            json_dict['new_lottery'] = nl
            data_list.append(json_dict)
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class WillSaleView(View):
    '''即将预售/正在公示/正在登记/最新摇号/无需摇号(不限购)'''

    def get(self, request):
        if request.GET.get('jzzzw') == '即将预售':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='即将预售').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['only_id'] = i['id']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']

                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jzzzw') == '正在公示':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='即将摇号').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jzzzw') == '正在登记':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='摇号剩余').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jzzzw') == '最新摇号':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='热门楼盘').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jzzzw') == '无需摇号':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='无需摇号').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jzzzw') == '已摇号':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='已摇号').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jzzzw') == '等待摇号':
            try:
                query_data = BuildingDetial.objects.values().filter(sale_stage='等待摇号').order_by('-attention_degree')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = i['building_name']
                    json_dict['building_create_time'] = i['building_create_time']
                    json_dict['attention_degree'] = i['attention_degree']
                    json_dict['comment_count'] = i['comment_count']
                    json_dict['sale_stage'] = i['sale_stage']
                    # json_dict['unit_price'] = i['unit_price']
                    json_dict['unit_price'] = i['open_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)


class OnlineSaleBuildingView(View):
    '''线上售楼部/摇红盘/热门公寓/地铁房/刚需房/改善房/在未来/优质/倒挂/本月热度/为你推荐/'''

    def get(self, request):
        try:
            req = request.GET.get('other')  # 线上售楼处
            query_data = BuildingDetial.objects.values().filter(budling_other__name=req).order_by('-create_time')
            # query_data = BuildingDetial.objects.values().filter(sale_stage=req)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']
                json_dict['building_name'] = i['building_name']
                json_dict['only_id'] = i['id']
                json_dict['building_create_time'] = i['building_create_time']
                json_dict['attention_degree'] = i['attention_degree']
                json_dict['comment_count'] = i['comment_count']
                json_dict['sale_stage'] = i['sale_stage']
                # json_dict['unit_price'] = i['unit_price']  ????
                json_dict['unit_price'] = i['open_price']
                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneKeyFindHouseView(View):
    '''一键找房'''

    def post(self, request):
        # return JsonResponse({"statue":200,"data":100},safe=False)
        try:
            page = request.POST.get('page') or 1
            land = request.POST.get('land_id') or '0'  # 区域 1,2,3
            train = request.POST.get('train_id') or '0'
            house = request.POST.get('house') or '0'  # 户型  1,2,3,4,5
            # 预算 单价/总价 D/Z
            money = request.POST.get('money') or '0'

            # 面积 数字
            area = request.POST.get('area') or '0'

            req = BuildingDetial.objects.all()
            if train is not None and train != '0':
                req = BuildingDetial.objects.filter(**{'train_id__in': [int(i) for i in train.split(',') if i != '0']})
            if land is not None and land != '0':
                req = BuildingDetial.objects.filter(**{'land_id__in': [int(i) for i in land.split(',') if i != '0']})
            if house is not None and house != '0':
                house = [{'house_section__icontains': i + '室'} for i in request.POST.get('house').split(',')]
                houseq = Q()
                houseq.connector = 'OR'
                for h in house:
                    houseq.children.append(('house_section__icontains', h['house_section__icontains']))
                req = req.filter(houseq)
            if money is not None and money != 0:
                moneys = money.split(',')
                if moneys[0] == 'D':
                    startmoney, endmoney = moneys[1].split('-')
                    req = req.annotate(
                        unit_price_as_int=Cast('unit_price', output_field=IntegerField())
                    )
                    req = req.filter(Q(unit_price_as_int__gte=startmoney) and Q(unit_price_as_int__lte=endmoney))
                if moneys[0] == 'Z':
                    startmoney, endmoney = moneys[1].split('-')
                    req = req.annotate(
                        total_price_as_int=Cast('total_price', output_field=IntegerField())
                    )
                    req = req.filter(Q(total_price_as_int__gte=startmoney) and Q(total_price_as_int__lte=endmoney))

            if not req.exists():
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            paginator = Paginator(req, 10)
            try:
                page_value = paginator.page(int(page))
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data = [{
                'only_id': i.id,
                'building_name': i.building_name,
                'comment_count': i.comment_count,
                'sale_stage': i.sale_stage,
                'train_id': i.train_id,
                'unit_price': i.unit_price,
                'land_id': LandDistrict.objects.get(id=i.land_id).name if i.land_id else '',
                'img': [i for i in BuildingImage.objects.filter(fk_id=i.id).values('photo_image')]
            }
                for i in page_value]

            return JsonResponse({"statue": 'success', 'data': data, 'Count': total_page}, safe=False)
        except Exception as e:
            return JsonResponse({"Result": 'false', 'Msg': str(e)})



class FilterQueryView(View):
    '''筛选查询'''

    def post(self, request):
        try:
            json_dict = {}
            json_dict['building_classfiy'] = request.POST.get('building_classfiy')
            json_dict['decorate_situation'] = request.POST.get('decorate_situation')
            json_dict['house_section__icontains'] = request.POST.get('house_section__icontains')
            json_dict['land_id'] = request.POST.get('land_id')
            json_dict['open_house_section__icontains'] = request.POST.get('open_house_section__icontains')

            # return JsonResponse({"statue":200,"data":json_dict},safe=False)
            page = json_dict.get('page') or 1
            od = json_dict.get('order_by') or 'create_time'

            # 去除空值
            datas = {}
            for o in json_dict:
                if json_dict[o]:
                    datas[o] = json_dict[o]
            # return JsonResponse({"statue":200,"data":datas},safe=False)
            query_list = {}
            if not datas:
                req = BuildingDetial.objects.order_by(od).values()
                query_list = list(req)
            else:
                req = BuildingDetial.objects.filter(**datas).order_by(od).values()
                query_list = list(req)

            # return JsonResponse({"statue":200,"data":query_list},safe=False)
            # 定义分页，每页实现为10
            paginator = Paginator(query_list, 10)

            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages

            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['land_id']
                query_other_data = LandDistrict.objects.filter(id=a).values()
                if len(query_other_data) == 0:
                    json_dict['land_id'] = ''
                else:
                    json_dict['land_id'] = query_other_data[0]['name']

                json_dict['only_id'] = i['id']
                json_dict['building_name'] = i['building_name']
                json_dict['comment_count'] = i['comment_count']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['train_id'] = i['train_id']
                # json_dict['unit_price'] = i['unit_price']
                json_dict['unit_price'] = i['open_price']
                build_id = i['id']
                fly = VRAerialPhotoAllPingImage.objects.filter(fuck_id=build_id).values('image_url')
                flylist = list(fly)
                for fff in flylist:
                    json_dict['fly'] = fff
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)


class MiddlePersonTopThreeView(View):
    '''首页优秀置业顾问'''

    def get(self, request):
        try:
            req = MiddlePeople.objects.all().order_by('-live_limit').values('id', 'building_fk_id', 'header_img',
                                                                            'bussiness_building', 'really_name',
                                                                            'user_fk_id')
            data_list = []
            for i in req[:3]:
                json_dict = {}
                a = i['user_fk_id']
                b = i['building_fk_id']
                bd = BuildingDetial.objects.get(id=b)
                ld = bd.land_id
                land = LandDistrict.objects.get(id=ld)
                json_dict['land_name'] = land.name
                d = Users.objects.get(id=a)
                json_dict['room_number'] = d.chat_room
                json_dict['header_img'] = i['header_img']
                json_dict['mp_id'] = i['id']
                json_dict['ur_id'] = a
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['really_name'] = i['really_name']
                data_list.append(json_dict)
            if req == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)


class AttentionView(View):
    '''首页我关注楼盘'''

    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            ureq = AttentionVillage.objects.filter(user_id=user_id).values('building_id')
            user = list(ureq)
            user_list = []
            for a in user:
                aa = a['building_id']
                user_list.append(aa)
            data = BuildingDetial.objects.filter(id__in=user_list).values(
                'land_id', 'building_name', 'id', 'building_create_time',
                'attention_degree', 'sale_stage', 'unit_price', 'comment_count'
            )
            build_list = list(data)
            paginator = Paginator(build_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            # last_list = []
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']
                json_dict['building_name'] = i['building_name']
                json_dict['only_id'] = i['id']
                json_dict['building_create_time'] = i['building_create_time']
                json_dict['attention_degree'] = i['attention_degree']
                json_dict['comment_count'] = i['comment_count']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['unit_price'] = i['unit_price']
                # json_dict['all_count'] = user_list
                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                data_list.append(json_dict)
            if build_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingDetialView(View):
    '''楼盘详情页'''

    def get(self, request):
        # 头/房源类型/销售状态/开盘信息/摇号结果/楼盘详细信息/
        try:
            req = request.GET.get('only_id')
            query_data = BuildingDetial.objects.values().filter(id=req)
            query_list = list(query_data)
            data_list = []
            for i in query_list:
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

                mp = MiddlePeople.objects.filter(building_fk_id=req).values('id')
                mp_list = list(mp)
                for i_ in mp_list:
                    json_dict['mp_id'] = i_['id']
                ii_house = i['house_count']  # 房源类型
                house_count = ii_house.split(',')
                json_dict['house_count'] = house_count
                ii_people = i['people_count']  # 报名人数
                people_count = ii_people.split(',')
                json_dict['people_count'] = people_count
                ii_win = i['win_probability']  # 摇中概率
                win_probability = ii_win.split(',')
                json_dict['win_probability'] = win_probability
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
                json_dict['land'] = i.get('land_id') and LandDistrict.objects.get(pk=i.get('land_id')).name or i.get(
                    'land_id')
                #
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''关注楼盘'''

    def post(self, request):
        try:
            user = request.POST.get('user_id')  # 用户id
            building = request.POST.get('building_id')  # 楼盘id
            count = AttentionVillage.objects.filter(user_id=user).count()
            # if count > 0:
            #     return JsonResponse({"statue": 'success', 'if_attention': 'NO'}, safe=False)
            AttentionVillage.objects.create(
                building_id=building,
                user_id=user
            )
            if_att = AttentionVillage.objects.filter(user_id=user).values('building_id')
            if_at_list = list(if_att)
            for i in if_at_list:
                if i == building:
                    return JsonResponse({"statue": 'success', 'if_attention': 'YES'}, safe=False)
            return JsonResponse({"statue": 'success', 'data': '关注成功', 'if_attention': 'YES'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class VillageDynamicView(View):
    '''楼盘动态'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            data = IssueBuildingDynamicMessage.objects.values().filter(building_detial__id=req).order_by(
                '-message_create_time')
            query_list = list(data)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            context = {"Status": 'success', 'Data': query_list}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''发表动态'''

    def post(self, request):
        try:
            fk_id = request.POST.get('only_id')  # 楼盘id
            choice_classfiy = request.POST.get('choice_classfiy')  # 选择类型 (0, 开盘)
            title = request.POST.get('title')  # 标题
            content = request.POST.get('content')  # 内容
            img = request.POST.get('img')  # 图片
            author = request.POST.get('author')  # 作者
            author_id = request.POST.get('author_id')

            IssueBuildingDynamicMessage.objects.values().create(building_detial_id=fk_id, title=title, content=content,
                                                                choice_classfiy=choice_classfiy, img=img, author=author,
                                                                author_id=author_id)
            return JsonResponse({"statue": 'success', 'data': '上传成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class VsView(View):
    '''VS列表'''

    def get(self, request):
        try:
            id = request.GET.get('only_id')
            query_data_one = BuildingDetial.objects.values().filter(id=id)
            query_list = list(query_data_one)
            for i in query_list:
                money = int(i['unit_price'])
                start_money = str(money - 5000)
                end_money = str(money + 5000)
                query_other_data1 = BuildingDetial.objects.values().filter(unit_price__gte=start_money).filter(
                    unit_price__lte=end_money)
                query_data_list = list(query_other_data1)  # 过滤前的查询集
                # 分页
                paginator = Paginator(query_data_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for b in page_value:
                    json_dict = {}
                    a = b['land_id']
                    query_other_data = LandDistrict.objects.values().get(id=a)
                    json_dict['land_id'] = query_other_data['name']
                    json_dict['building_name'] = b['building_name']
                    json_dict['dangqian_id'] = b['id']
                    json_dict['sale_stage'] = b['sale_stage']
                    json_dict['unit_price'] = b['unit_price']
                    build_id = i['id']
                    im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                    im_list = list(im)
                    for aaa in im_list:
                        json_dict['img'] = aaa
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    # 取关
    def post(self, request):
        try:
            user = request.POST.get('user_id')  # 用户id
            building = request.POST.get('building_id')  # 楼盘id
            AttentionVillage.objects.filter(Q(building_id=building) & Q(user_id=user)).delete()
            return JsonResponse({"statue": 'success', 'data': '取关了'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class VsDetialView(View):
    '''Vs详情页'''

    def get(self, request):
        try:
            present = request.GET.get('present_id')
            choice = request.GET.get('choice_id')
            data = BuildingDetial.objects.values().filter(id=present)
            present_data = list(data)
            present_list = []
            for i in present_data:
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
                json_dict['cool_captial_request'] = i['cool_captial_request']  # 验资金额
                json_dict['covered_tier'] = i['covered_tier']  # 层高
                json_dict['stall_message'] = i['stall_message']  # 车位数
                json_dict['upstart'] = i['upstart']  # 开发商
                json_dict['decorate_situation'] = i['decorate_situation']  # 装修
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']  # 所在区域
                json_dict['green_rate'] = i['green_rate']  # 绿化率
                json_dict['equity_year'] = i['equity_year']  # 产权年限
                json_dict['volume_rate'] = i['volume_rate']  # 容积率
                json_dict['delivery_time'] = i['delivery_time']  # 交房时间
                json_dict['building_classfiy'] = i['building_classfiy']  # 楼盘类型
                json_dict['company_money'] = i['company_money']  # 物业费
                json_dict['company'] = i['company']  # 物业公司
                b = i['train_id']
                query_other_data3 = SubwayStation.objects.values().get(id=b)
                json_dict['train_id'] = query_other_data3['name']  # 地铁站
                present_list.append(json_dict)
            data2 = BuildingDetial.objects.values().filter(id=choice)
            choice_data = list(data2)
            choice_list = []
            for i in choice_data:
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
                json_dict['cool_captial_request'] = i['cool_captial_request']  # 验资金额
                json_dict['covered_tier'] = i['covered_tier']  # 层高
                json_dict['stall_message'] = i['stall_message']  # 车位数
                json_dict['upstart'] = i['upstart']  # 开发商
                json_dict['decorate_situation'] = i['decorate_situation']  # 装修
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']  # 所在区域
                json_dict['green_rate'] = i['green_rate']  # 绿化率
                json_dict['equity_year'] = i['equity_year']  # 产权年限
                json_dict['volume_rate'] = i['volume_rate']  # 容积率
                json_dict['delivery_time'] = i['delivery_time']  # 交房时间
                json_dict['building_classfiy'] = i['building_classfiy']  # 楼盘类型
                json_dict['company_money'] = i['company_money']  # 物业费
                json_dict['company'] = i['company']  # 物业公司
                b = i['train_id']
                query_other_data3 = SubwayStation.objects.values().get(id=b)
                json_dict['train_id'] = query_other_data3['name']  # 地铁站
                # present_list.append(json_dict)
                choice_list.append(json_dict)
            context = {"Status": 'success', 'Data': present_list, 'Data2': choice_list}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingHouseDetialView(View):
    '''楼盘详细信息'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = BuildingDetial.objects.values().filter(id=req)
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['building_name'] = i['building_name']  # 楼盘名称
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']  # 地区名称
                json_dict['ave_price'] = i['unit_price']  # 参考单价
                json_dict['sale_stage'] = i['sale_stage']  # 销售状态
                json_dict['cube_count'] = i['cube_count']  # 整栋数
                json_dict['tier_condition'] = i['tier_condition']  # 楼层状况
                json_dict['company_money'] = i['company_money']  # 物业费
                json_dict['house_section'] = i['house_section']  # 主力户型
                json_dict['sale_building_location'] = i['sale_building_location']  # 售楼地址
                json_dict['premises_location'] = i['premises_location']  # 楼盘地址
                json_dict['delivery_time'] = i['delivery_time']  # 交房时间
                json_dict['building_nickname'] = i['building_nickname']  # 楼盘别名
                json_dict['building_classfiy'] = i['building_classfiy']  # 楼盘类型
                json_dict['equity_year'] = i['equity_year']  # 产权年限
                json_dict['decorate_situation'] = i['decorate_situation']  # 装修
                json_dict['green_rate'] = i['green_rate']  # 绿化率
                json_dict['volume_rate'] = i['volume_rate']  # 容积率
                json_dict['stall_message'] = i['stall_message']  # 车位信息
                json_dict['all_house_count'] = i['all_house_count']  # 总户数
                json_dict['floor_space'] = i['floor_space']  # 占地面积
                json_dict['covered_area'] = i['covered_area']  # 建筑面积
                json_dict['company'] = i['company']  # 物业公司
                json_dict['upstart'] = i['upstart']  # 开发商
                json_dict['train_traffic'] = i['train_traffic']  # 地铁交通
                json_dict['bus_site'] = i['bus_site']  # 公交站点
                json_dict['school'] = i['school']  # 学校
                json_dict['hospital'] = i['hospital']  # 医院
                json_dict['bank'] = i['bank']  # 银行
                json_dict['catering'] = i['catering']  # 餐饮
                json_dict['shopping'] = i['shopping']  # 购物
                json_dict['park'] = i['park']  # 公园
                json_dict['other_mating'] = i['other_mating']  # 其他
                json_dict['building_intro'] = i['building_intro']  # 楼盘简介
                json_dict['will_sale_number'] = i['will_sale_number']  # 预售证号
                json_dict['give_number_time'] = i['give_number_time']  # 发证时间
                json_dict['lottery_count'] = i['lottery_count']  # 摇号批次
                im = BuildingImage.objects.filter(fk_id=req).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class PublicityView(View):
    '''公示方案'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            data = PublicPlan.objects.values().filter(fk_id=req)
            query_list = list(data)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            context = {"Status": 'success', 'Data': query_list}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SmallVillageSellStateView(View):
    '''小滑块'''
    '''
    2019.12.10 , 12.14-12.16 , 12.17(08.12-01.01)暂无, 12.18暂无,12.20 10:00暂无, 08.31
    '''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            data = BuildingStatueTimeSale.objects.values().filter(fk_id=req)
            query_list = list(data)
            last_list = []
            for k, i in enumerate(query_list):
                json_dict = {}
                try:
                    year = str(i['will_sale_time']).split('.')[0]
                    # year = str(datetime.datetime.now().date()).split('-')[0]
                except:
                    return JsonResponse({'Statue': 200, 'Msg': '当前销售时间为空', 'Data': last_list})
                time_now = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d').date()
                # print(time_now)

                # 1
                try:
                    will_sale_time = datetime.datetime.strptime(str(i['will_sale_time']), '%Y.%m.%d').date()
                    j = time_now - will_sale_time
                    if j.days > 0:
                        json_dict['will_sale_time'] = i['will_sale_time']  # 2019.12.10
                        last_list.append(json_dict)
                    else:
                        return JsonResponse({'Statue': 200, 'Msg': 0, 'Data': last_list})
                except:
                    return JsonResponse({'Statue': 200, 'Msg': 0, 'Data': last_list})

                # 2
                try:
                    r_t = i['register_time'].split('-')
                    begin = datetime.datetime.strptime(year + '.' + r_t[0], '%Y.%m.%d').date()
                    end = datetime.datetime.strptime(year + '.' + r_t[1], '%Y.%m.%d').date()
                    k = time_now - begin
                    if k.days > 0:
                        json_dict['register_time'] = i['register_time']  # 12.14-12.16
                        last_list.append(json_dict)
                    else:
                        return JsonResponse({'Statue': 200, 'Msg': 1, 'Data': last_list})
                except:
                    return JsonResponse({'Statue': 200, 'Msg': 1, 'Data': last_list})

                # 3
                if i['commit_time'] == '暂无':
                    json_dict['commit_time'] = i['commit_time']
                    last_list.append(json_dict)

                    continue

                else:
                    try:
                        c_t = i['commit_time'].split('-')
                        # print(c_t)
                        if len(c_t) < 2:  # 只有一个日子
                            try:
                                commit_time = datetime.datetime.strptime(year + '.' + c_t[0], '%Y.%m.%d').date()
                                jj = time_now - commit_time
                                if jj.days > 0:
                                    json_dict['commit_time'] = i['commit_time']  # 2019.12.10
                                    last_list.append(json_dict)
                                else:
                                    return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                            except:
                                return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                        else:  # 俩日子
                            print('else')
                            try:
                                commit_time_begin = datetime.datetime.strptime(year + '.' + c_t[0], '%Y.%m.%d').date()
                                commit_time_end = datetime.datetime.strptime(year + '.' + c_t[1], '%Y.%m.%d').date()
                                # commit_timestart_time = datetime.datetime.strptime(commit_time_begin, '%m.%d')  # %Y-%m-%d
                                # commit_timeend_time = datetime.datetime.strptime(commit_time_end, '%m.%d')
                                k = time_now - commit_time_begin
                                if k.days > 0:
                                    json_dict['commit_time'] = i['commit_time']  # 12.14-12.16
                                    last_list.append(json_dict)
                                else:
                                    return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                            except:
                                return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                    except:
                        return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})

                # 4
                if i['want_told_time'] == '暂无':
                    json_dict['want_told_time'] = i['want_told_time']
                    last_list.append(json_dict)

                    continue

                else:
                    try:
                        want_told_time = datetime.datetime.strptime(year + '.' + str(i['want_told_time']),
                                                                    '%Y.%m.%d').date()
                        jjj = time_now - want_told_time
                        if jjj.days > 0:
                            json_dict['want_told_time'] = i['want_told_time']  # 2019.12.10
                            last_list.append(json_dict)
                        else:
                            return JsonResponse({'Statue': 200, 'Msg': 3, 'Data': last_list})
                    except:
                        return JsonResponse({'Statue': 200, 'Msg': 3, 'Data': last_list})

                # 5
                if i['lottery_time'] == '暂无':
                    json_dict['lottery_time'] = i['lottery_time']
                else:
                    try:
                        l_t = i['lottery_time'].split(' ')
                        lottery_time = datetime.datetime.strptime(year + '.' + l_t[0], '%Y.%m.%d').date()
                        jjjj = time_now - lottery_time  # 12.20 10:00
                        if jjjj.days > 0:
                            json_dict['lottery_time'] = i['lottery_time']
                            last_list.append(json_dict)
                        else:
                            return JsonResponse({'Statue': 200, 'Msg': 4, 'Data': last_list})
                    except:
                        return JsonResponse({'Statue': 200, 'Msg': 4, 'Data': last_list})

                # 6
                try:
                    choice_house_time = datetime.datetime.strptime(str(i['choice_house_time']), '%Y.%m.%d').date()
                    jjjjj = time_now - choice_house_time
                    if jjjjj.days > 0:
                        json_dict['choice_house_time'] = i['choice_house_time']
                        last_list.append(json_dict)
                    else:
                        return JsonResponse({'Statue': 200, 'Msg': 5, 'Data': last_list})
                except:
                    return JsonResponse({'Statue': 200, 'Msg': 5, 'Data': last_list})

                last_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            # wa = list(set(last_list))
            wa = last_list
            context = {"Status": 'success', 'Data': wa}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''历史摇号详情页小滑块'''

    def post(self, request):
        try:
            req = request.POST.get('only_id')
            hid = request.POST.get('history_id')
            data = BuildingStatueTimeSale.objects.values().filter(Q(fk_id=req) & Q(history_id=hid))
            query_list = list(data)
            last_list = []
            for k, i in enumerate(query_list):
                json_dict = {}
                try:
                    year = str(i['will_sale_time']).split('.')[0]
                    # year = str(datetime.datetime.now().date()).split('-')[0]
                except:
                    return JsonResponse({'Statue': 200, 'Msg': '当前销售时间为空', 'Data': last_list})
                time_now = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d').date()
                # print(time_now)

                # 1
                try:
                    will_sale_time = datetime.datetime.strptime(str(i['will_sale_time']), '%Y.%m.%d').date()
                    j = time_now - will_sale_time
                    if j.days > 0:
                        json_dict['will_sale_time'] = i['will_sale_time']  # 2019.12.10
                        last_list.append(json_dict)
                    else:
                        return JsonResponse({'Statue': 200, 'Msg': 0, 'Data': last_list})
                except:
                    return JsonResponse({'Statue': 200, 'Msg': 0, 'Data': last_list})

                # 2
                try:
                    r_t = i['register_time'].split('-')
                    begin = datetime.datetime.strptime(year + '.' + r_t[0], '%Y.%m.%d').date()
                    end = datetime.datetime.strptime(year + '.' + r_t[1], '%Y.%m.%d').date()
                    k = time_now - begin
                    if k.days > 0:
                        json_dict['register_time'] = i['register_time']  # 12.14-12.16
                        last_list.append(json_dict)
                    else:
                        return JsonResponse({'Statue': 200, 'Msg': 1, 'Data': last_list})
                except:
                    return JsonResponse({'Statue': 200, 'Msg': 1, 'Data': last_list})

                # 3
                if i['commit_time'] == '暂无':
                    json_dict['commit_time'] = i['commit_time']
                    last_list.append(json_dict)

                    continue

                else:
                    try:
                        c_t = i['commit_time'].split('-')
                        # print(c_t)
                        if len(c_t) < 2:  # 只有一个日子
                            try:
                                commit_time = datetime.datetime.strptime(year + '.' + c_t[0], '%Y.%m.%d').date()
                                jj = time_now - commit_time
                                if jj.days > 0:
                                    json_dict['commit_time'] = i['commit_time']  # 2019.12.10
                                    last_list.append(json_dict)
                                else:
                                    return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                            except:
                                return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                        else:  # 俩日子
                            print('else')
                            try:
                                commit_time_begin = datetime.datetime.strptime(year + '.' + c_t[0], '%Y.%m.%d').date()
                                commit_time_end = datetime.datetime.strptime(year + '.' + c_t[1], '%Y.%m.%d').date()
                                # commit_timestart_time = datetime.datetime.strptime(commit_time_begin, '%m.%d')  # %Y-%m-%d
                                # commit_timeend_time = datetime.datetime.strptime(commit_time_end, '%m.%d')
                                k = time_now - commit_time_begin
                                if k.days > 0:
                                    json_dict['commit_time'] = i['commit_time']  # 12.14-12.16
                                    last_list.append(json_dict)
                                else:
                                    return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                            except:
                                return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})
                    except:
                        return JsonResponse({'Statue': 200, 'Msg': 2, 'Data': last_list})

                # 4
                if i['want_told_time'] == '暂无':
                    json_dict['want_told_time'] = i['want_told_time']
                    last_list.append(json_dict)

                    continue

                else:
                    try:
                        want_told_time = datetime.datetime.strptime(year + '.' + str(i['want_told_time']),
                                                                    '%Y.%m.%d').date()
                        jjj = time_now - want_told_time
                        if jjj.days > 0:
                            json_dict['want_told_time'] = i['want_told_time']  # 2019.12.10
                            last_list.append(json_dict)
                        else:
                            return JsonResponse({'Statue': 200, 'Msg': 3, 'Data': last_list})
                    except:
                        return JsonResponse({'Statue': 200, 'Msg': 3, 'Data': last_list})

                # 5
                if i['lottery_time'] == '暂无':
                    json_dict['lottery_time'] = i['lottery_time']
                else:
                    try:
                        l_t = i['lottery_time'].split(' ')
                        lottery_time = datetime.datetime.strptime(year + '.' + l_t[0], '%Y.%m.%d').date()
                        jjjj = time_now - lottery_time  # 12.20 10:00
                        if jjjj.days > 0:
                            json_dict['lottery_time'] = i['lottery_time']
                            last_list.append(json_dict)
                        else:
                            return JsonResponse({'Statue': 200, 'Msg': 4, 'Data': last_list})
                    except:
                        return JsonResponse({'Statue': 200, 'Msg': 4, 'Data': last_list})

                # 6
                try:
                    choice_house_time = datetime.datetime.strptime(str(i['choice_house_time']), '%Y.%m.%d').date()
                    jjjjj = time_now - choice_house_time
                    if jjjjj.days > 0:
                        json_dict['choice_house_time'] = i['choice_house_time']
                        last_list.append(json_dict)
                    else:
                        return JsonResponse({'Statue': 200, 'Msg': 5, 'Data': last_list})
                except:
                    return JsonResponse({'Statue': 200, 'Msg': 5, 'Data': last_list})

                last_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            # wa = list(set(last_list))
            wa = last_list
            context = {"Status": 'success', 'Data': wa}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IntentRegisterView(View):
    '''意向登记列表页'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')  # UnionLotteryResult
            data = ToldPurpose.objects.values().filter(fk_id=req)
            # data = ToldPurpose.objects.values().filter(fk_id=req)
            query_list = list(data)
            a = {}
            data_list = []
            for i in query_list[0:11]:
                a['lottery_number'] = i['buy_house_number']
                a['lottery_name'] = i['lottery_name']
                a['create_time'] = i['create_time']
                a['ID_number'] = i['ID_number']
                a['other_lottery_name'] = i['other_lottery_name']
                a['other_ID_number'] = i['other_ID_number']
                a['audit_status'] = i['audit_status']
                a['if_win_lottery'] = i['if_win_lottery']
                data_list.append(a)
            # j = {}
            # j['data'] = data_list
            # n_l.append(j)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            context = {"Status": 'success', 'Data': data_list}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuildingLotteryResultView(View):
    '''摇号结果'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            try:
                nm = request.GET.get('buy_house_number')
                ur = request.GET.get('ur_id')
                d = LotteryResult.objects.get(buy_house_number=nm)
                union = MiddleUnionId.objects.get(fk_id=ur)
                bd = BuildingDetial.objects.get(id=req)
                yaohaojieguotongzhi(union.gong_open_id, bd.building_name, nm, '')
            except:
                return JsonResponse({'Statue': 'False', 'Msg': '用户本期未中签'})

            data = ToldPurpose.objects.values().filter(village_name__id=req).filter(if_win_lottery='1')
            all_value = BuildingDetial.objects.values().filter(id=req)
            name_list = list(all_value)
            query_list = list(data)
            a = {}
            data_list = []
            for i in name_list:
                a['building_name'] = i['building_name']
                a['house_count'] = i['house_count']
                a['people_count'] = i['people_count']
                a['win_probability'] = i['win_probability']
                data_list.append(a)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            context = {"Status": 'success', 'Data': data_list}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''摇号结果楼盘详情页列表显示10条'''

    def post(self, request):
        try:
            req = request.POST.get('only_id')
            query_data = LotteryResult.objects.values().filter(fk_id=req).order_by('-serial_number')
            query_list = list(query_data)
            data_list = []
            for i in query_list[0:11]:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['fk_id'] = i['fk_id']
                json_dict['pid'] = i['pid']
                json_dict['serial_number'] = i['serial_number']
                json_dict['buy_house_number'] = i['buy_house_number']
                b = ToldPurpose.objects.filter(buy_house_number=i['buy_house_number']).values('lottery_name',
                                                                                              'ID_number',
                                                                                              'other_lottery_name',
                                                                                              'other_ID_number',
                                                                                              'audit_status',
                                                                                              'if_win_lottery')
                for a in b:
                    json_dict['lottery_name'] = a['lottery_name']
                    json_dict['ID_number'] = a['ID_number']
                    json_dict['other_lottery_name'] = a['other_lottery_name']
                    json_dict['other_ID_number'] = a['other_ID_number']
                    json_dict['audit_status'] = a['audit_status']
                    json_dict['if_win_lottery'] = a['if_win_lottery']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"Statue": 'success', 'Data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SearchLotteryNumberView(View):
    '''搜索摇号'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            value = request.GET.get('value')
            data = ToldPurpose.objects.values().filter(village_name__id=req).filter(
                Q(ID_number=value) | Q(lottery_number=value))
            query_list = list(data)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            context = {"Status": 'success', 'Data': query_list}
            return JsonResponse(context)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''一房一价平面图'''

    def post(self, request):
        try:
            req = request.POST.get('only_id')  # 楼盘id
            yeq = request.POST.get('dong')  # 1,2,3
            yyeq = request.POST.get('yuan')  # 1,2,3
            dmeq = request.POST.get('ceng')  # 1,2,3
            data_list = []
            if all([req, yeq, yyeq, dmeq]):
                data_list = []
                mmeq = [i for i in dmeq]
                pd = {}
                menlist = []
                for mm in mmeq:
                    me = OneHouseOnePrice.objects.filter(
                        Q(building_detial_id=req) & Q(house_dong=yeq) & Q(house_yuan=yyeq) & Q(house_ceng=mm)).values()
                    if me:
                        melis = list(me)
                        jd = {'house_ceng': mm, 'men': melis}
                        menlist.append(jd)
                        pd['house_yuan'] = yyeq
                        pd['yuan'] = menlist
                    data_list.append(pd)
            # # 取单元号
            # qudanyuanhao = OneHouseOnePrice.objects.filter(Q(building_detial_id=req) & Q(house_dong=yeq)).values('id', 'house_yuan')
            # list_yuan = list(qudanyuanhao)
            # yuan_list = []
            # for yuan in list_yuan:
            #     yuan_dict = {}
            #     yid = yuan['id']
            #     yuan_dict['house_id'] = yid
            #     yuan_dict['house_yuan'] = yuan['house_yuan']
            #     # 取层数
            #     qucengshu = OneHouseOnePrice.objects.filter(house_yuan=yid).values()
            #     count = OneHouseOnePrice.objects.filter(house_yuan=yid).count()
            #     list_ceng = list(qucengshu)
            #     ceng_list = []
            #     for ceng in list_ceng:
            #         ceng_dict = {}
            #         cid = ceng['id']
            #         ceng_dict['ceng_id'] = cid
            #         ceng_dict['count'] = count
            #         d = BuildingDetial.objects.get(id=req) #sale_stage
            #         ceng_dict['sale_stage'] = d.sale_stage
            #         ceng_dict['unit_price'] = d.unit_price
            #         ceng_list.append(ceng_dict)
            #     yuan_dict['second'] = ceng_list
            #     yuan_list.append(yuan_dict)
            else:

                dong_list = [i for i in yeq]

                me = OneHouseOnePrice.objects.filter(
                    Q(building_detial_id=req) & Q(house_dong__in=dong_list)).values()
                data_list = [i for i in me]

            return JsonResponse({"statue": 'success', 'data': data_list, 'dong': yeq}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': str(e)}
            return JsonResponse(context)


class OneHouseOnePriceTitleListView(View):
    '''一房一价取楼号'''

    def get(self, request):
        import re
        try:
            req = request.GET.get('only_id')
            one = OneHouseOnePrice.objects.filter(building_detial_id=req).values('house_dong').distinct()
            rl = list(one)
            three = OneHouseOnePrice.objects.filter(building_detial_id=req).values('house_yuan').distinct()
            yl = list(three)
            two = OneHouseOnePrice.objects.filter(building_detial_id=req).values('door_number', 'id')
            tl = list(two)
            house_ceng = []
            for kk in tl:
                te = kk['door_number']
                m = re.findall("\d+", te)  # 匹配房号
                if m == []:  # 门0
                    house_ceng.append('0')

                elif len(m) == 1:  # 门1
                    if len(m[0]) == 1:
                        for i in m[0]:
                            house_ceng.append(i)
                    elif len(m[0]) == 2:
                        house_ceng.append(m[0])
                    elif len(m[0]) == 3:
                        if bool(re.search('[a-zA-Z]', te)) == True:  # 如果其中含有字母
                            house_ceng.append(m[0][0])
                        else:
                            house_ceng.append(m[0][0])
                    elif len(m[0]) == 4:
                        house_ceng.append(m[0][0] + m[0][1])

                elif len(m) == 2:  # 门2
                    if len(m[0]) == 1:
                        house_ceng.append(m[0])
                    elif len(m[0]) == 2:
                        house_ceng.append(m[0])
                    elif len(m[0]) == 3:
                        house_ceng.append(m[0][0])
                    elif len(m[0]) == 4:
                        house_ceng.append(m[0][0] + m[0][1])

                elif len(m) == 3:  # 门3
                    house_ceng.append(m[0])

                else:  # 门4
                    house_ceng.append(m[0])
            for dd, ddd in zip(tl, house_ceng):
                try:
                    OneHouseOnePrice.objects.filter(id=dd['id']).update(house_ceng=ddd)
                except:
                    OneHouseOnePrice.objects.filter(id=dd['id']).update(house_ceng='0')
            ttl = sorted([int(i) for i in set(house_ceng)])
            # data_ddd = [{'dong':rl, 'dv':['yuan':yl,'yv': ttl ]}]
            # data_ddd = [{
            #     'house_dong': rl,
            #     'dong':[{
            #         'house_yuan': yl,
            #         'ceng': [{
            #             'house_ceng': ttl
            #         }]
            #     }]
            # }]
            # return JsonResponse({"statue": 'success', 'dong': rl, 'yuan': yl, 'ceng': ttl}, safe=False)
            data_list = []
            for a1 in rl:
                aj = {}
                aj['house_dong'] = a1['house_dong']
                a2li = []
                for a2 in yl:
                    a2j = {}
                    a2j['house_yuan'] = a2['house_yuan']
                    a2j['ceng'] = ttl
                    a2li.append(a2j)
                aj['yuan'] = a2li
                data_list.append(aj)

            # return JsonResponse({"statue": 'success', 'dong': rl, 'yuan': yl, 'ceng': ttl}, safe=False)
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneHouseOnePriceListView(View):
    '''一房一价列表页'''

    def get(self, request):
        if request.GET.get('jd') == '0':
            try:
                req = request.GET.get('only_id')
                dong_number = []
                # data = OneHouseOnePrice.objects.values().filter(building_detial__id=req)
                data = OneHouseOnePrice.objects.values().filter(will_sale_number=req)
                for bb in data:
                    dong_number.append(bb['house_dong'])
                dong_number1 = set(dong_number)
                dong_number2 = list(dong_number1)  # 楼栋总数
                query_list = list(data)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)
            try:
                # 分页
                paginator = Paginator(query_list, 5)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['yfyj_id'] = i['id']
                    json_dict['house_dong'] = i['house_dong']
                    json_dict['house_yuan'] = i['house_yuan']
                    # json_dict['house_ceng'] = i['house_ceng']
                    json_dict['door_number'] = i['door_number']
                    # json_dict['decorate_type'] = i['decorate_type']
                    json_dict['one_price'] = i['one_price']
                    json_dict['all_price'] = i['all_price']
                    json_dict['area'] = i['in_area']
                    # json_dict['decorate_type_price'] = i['decorate_type_price']
                    try:
                        json_dict['result1'] = int(i['all_price']) * 0.3
                        json_dict['result2'] = int(i['all_price']) * 0.6
                    except:
                        json_dict['result1'] = '暂无'
                        json_dict['result2'] = '暂无'
                    json_dict['dong_count'] = dong_number2
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jd') == '2':
            try:
                req = request.GET.get('only_id')
                # 取栋号
                one = OneHouseOnePrice.objects.filter(building_detial__id=req).values('id', 'house_dong')
                rl = list(one)
                # i = rl[0]['id']
                last_append = []

                for rli in rl:
                    # data_dict = {}
                    i = rli['id']
                    # do = rl[0]['house_dong']
                    do = rli['house_dong']
                    # 取单元号
                    two = OneHouseOnePrice.objects.filter(Q(building_detial_id=req) & Q(id=i)).values('id',
                                                                                                      'house_yuan')
                    tl = list(two)

                    one_list = []
                    for t in tl:
                        tid = t['id']
                        # 取层号
                        ceng = OneHouseOnePrice.objects.filter(Q(building_detial_id=req) & Q(id=tid)).values('id',
                                                                                                             'house_ceng')
                        liceng = list(ceng)
                        two_l = []
                        for ce in liceng:
                            cid = ce['id']
                            # 取门
                            pdm = OneHouseOnePrice.objects.filter(id=cid).values()
                            # sub_listt = pdm.subs.all()
                            # 序列化市或区数据
                            sub_list = []
                            for sub_model in pdm:
                                sub_list.append({'id': sub_model['id'], 'door_number': sub_model['door_number']})
                            sub_data = {
                                'ceng': ce['house_ceng'],
                                'door': sub_list
                            }
                            two_l.append(sub_data)
                        three_data = {
                            'yuan': t['house_yuan'],
                            'ceng': two_l
                        }
                        one_list.append(three_data)
                    one_data = {
                        'dong': do,
                        'yuan': one_list
                    }

                    # data_dict['data'] = one_data
                    last_append.append(one_data)
                    # return JsonResponse({"statue": 'success', 'data': one_data}, safe=False)
                return JsonResponse({"statue": 'success', 'data': last_append}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

        elif request.GET.get('jd') == '1':
            try:
                req = request.GET.get('only_id')
                one = OneHouseOnePrice.objects.filter(building_detial_id=req).values('water_money', 'area',
                                                                                     'house_ceng', 'house_dong', 'id',
                                                                                     'house_yuan', 'door_number',
                                                                                     'house_xing', 'one_price')
                data_list = list(one)
                query_list = []
                print(one)
                for i in data_list:
                    one_dict = {}
                    li = []
                    a = i['id']
                    one_dict['id'] = i['id']
                    one_dict['house_dong'] = i['house_dong']
                    one_dict['house_yuan'] = i['house_yuan']
                    two_dict = {}
                    two_dict['house_ceng'] = i['house_ceng']
                    two_dict['door_number'] = i['door_number']
                    two_dict['house_xing'] = i['house_xing']
                    two_dict['one_price'] = i['one_price']
                    two_dict['water_money'] = i['water_money']
                    two_dict['area'] = i['area']
                    li.append(two_dict)
                    one_dict['data'] = li
                    query_list.append(one_dict)
                if data_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': query_list}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            # bd = json_dict.get('only_id')
            p = json_dict.get('page')
            d = json_dict.get('house_dong')
            x = json_dict.get('house_xing')
            b = json_dict.get('only_id')
            data = OneHouseOnePrice.objects.filter(Q(house_dong=d) | Q(house_xing=x) & Q(building_detial_id=b)).values()
            query_list = list(data)
            paginator = Paginator(query_list, 5)
            page = int(p)
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['yfyj_id'] = i['id']
                json_dict['house_dong'] = i['house_dong']
                json_dict['house_yuan'] = i['house_yuan']
                json_dict['house_ceng'] = i['house_ceng']
                json_dict['door_number'] = i['door_number']
                json_dict['decorate_type'] = i['decorate_type']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['area'] = i['area']
                json_dict['decorate_type_price'] = i['decorate_type_price']
                # json_dict['result'] = i['result']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class OneHouseOnePriceDetailView(View):
    '''一房一价详情页'''

    def get(self, request):
        try:
            req = request.GET.get('yfyj_id')
            building_name = request.GET.get('name')  # 楼盘名称
            data = OneHouseOnePrice.objects.values().filter(id=req)
            query_list = list(data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['house_dong'] = i['house_dong']
                json_dict['house_yuan'] = i['house_yuan']
                json_dict['door_number'] = i['door_number']
                json_dict['create_area'] = i['create_area']
                json_dict['in_area'] = i['in_area']
                json_dict['gave_house'] = i['gave_house']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['will_sale_number'] = i['will_sale_number']
                json_dict['building_name'] = building_name
                json_dict['public_date'] = i['public_date']
                json_dict['give_date'] = i['give_date']
                json_dict['build_company'] = i['build_company']
                json_dict['lottery_title'] = i['lottery_title']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''一房一价排序'''

    def post(self, request):
        try:
            bd = request.POST.get('only_id')
            ob = request.POST.get('order_by')
            data = OneHouseOnePrice.objects.filter(building_detial_id=bd).values().order_by(ob)
            query_list = list(data)
            paginator = Paginator(query_list, 5)
            page = int(request.POST.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['yfyj_id'] = i['id']
                json_dict['house_dong'] = i['house_dong']
                json_dict['house_yuan'] = i['house_yuan']
                json_dict['house_ceng'] = i['house_ceng']
                json_dict['door_number'] = i['door_number']
                json_dict['decorate_type'] = i['decorate_type']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['area'] = i['area']
                json_dict['decorate_type_price'] = i['decorate_type_price']
                # json_dict['result'] = i['result']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SystemMessageView(View):
    '''系统消息(所有公示方案/摇号结果)'''

    def get(self, request):
        try:
            if request.GET.get('system') == '系统消息':
                data = PublicPlan.objects.values().all().order_by('-create_time')
                query_list = list(data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['fk_id'] = i['fk_id']
                    json_dict['title'] = i['title']
                    json_dict['content'] = i['content']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''生成一房一价图'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingOneHouseOnePriceImage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MiddleTuiView(View):
    '''详情页置业顾问推荐'''

    def get(self, request):
        try:
            bd = request.GET.get('only_id')
            req = MiddlePeople.objects.filter(building_fk_id=bd).values('id', 'header_img', 'bussiness_building',
                                                                        'really_name').order_by('-live_limit')
            data_list = []
            for i in req[:3]:
                json_dict = {}
                json_dict['mp_id'] = i['id']
                json_dict['header_img'] = i['header_img']
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['really_name'] = i['really_name']
                data_list.append(json_dict)
            if req == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''一房一价画图接口'''

    def post(self, request):
        try:
            req = request.POST.get('only_id')
            deq = request.POST.get('cut_data')  # 1-1,2,3;2-1,2,3;3-1,2,3
            deql = deq.split(';')  # [1-1,2,3  1-1,2,3  1-1,2,3]
            a = [i.split('-') for i in deql]
            data_list = []
            for i in a:
                house_yuan = i[1].split(',')
                for ii in house_yuan:
                    jd1 = {}
                    house_dong = i[0]
                    jd1['house_dong'] = house_dong
                    jd1['house_yuan'] = ii
                    data = OneHouseOnePrice.objects.filter(
                        Q(building_detial_id=req) & Q(house_dong=house_dong) & Q(house_yuan=ii)).values(
                        'house_ceng').distinct()
                    dal = list(data)
                    dl3 = []
                    for iii in dal:  # 层
                        jd4 = {}
                        jd4['house_ceng'] = iii['house_ceng']
                        reqq = OneHouseOnePrice.objects.filter(
                            Q(building_detial_id=req) & Q(house_dong=house_dong) & Q(house_yuan=ii) & Q(
                                house_ceng=iii['house_ceng'])).values()
                        reqql = list(reqq)
                        jd4['sonsonson'] = reqql
                        dl3.append(jd4)
                    jd1['sonson'] = dl3
                    data_list.append(jd1)
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class NotSellPeopleView(View):
    '''售前顾问/联系置业顾问/更多置业顾问'''

    def get(self, request):
        try:
            bd = request.GET.get('only_id')
            req = MiddlePeople.objects.filter(building_fk_id=bd).values('id', 'header_img', 'bussiness_building',
                                                                        'really_name', 'browse_count', 'live_limit',
                                                                        'click_count', 'mobile').order_by('-live_limit')
            paginator = Paginator(req, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                query_data = BuildingDetial.objects.values().get(id=bd)
                json_dict['building_name'] = query_data['building_name']  # 楼盘名称
                json_dict['header_img'] = i['header_img']
                json_dict['bussiness_building'] = i['bussiness_building']
                json_dict['really_name'] = i['really_name']
                json_dict['browse_count'] = i['browse_count']
                json_dict['live_limit'] = i['live_limit']
                json_dict['click_count'] = i['click_count']
                json_dict['mobile'] = i['mobile']
                data_list.append(json_dict)
            if req == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class FirstCommentView(View):
    '''判断用户是否给该条楼盘评论点赞/文章点赞/问答点赞'''

    def get(self, request):
        try:
            cho = request.GET.get('choice')  # 点赞分类
            ur = request.GET.get('type_id')  # 需要确定的id
            if cho == '0':  # 该条楼盘评论点赞  传入楼盘id
                try:
                    bd = Comment.objects.filter(village_id=ur).values('id')  # 楼盘id
                    bdl = list(bd)
                    data_list = []
                    for i in bdl:
                        json_dict = {}
                        json_dict['zan_id'] = i['id']
                        data_list.append(json_dict)
                    if data_list == []:
                        return JsonResponse({"statue": 'success', 'data': '没有点过赞', 'judgement': False}, safe=False)
                    return JsonResponse({"statue": 'success', 'data': data_list, 'judgement': True}, safe=False)
                except:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            else:  # 文章点赞/问答点赞/顾问点赞/购房百科点赞
                try:
                    bd = ZanCount.objects.filter(Q(choice_classfiy=cho) & Q(type_id=ur)).count()  # 文章id
                    if bd > 0:
                        return JsonResponse({"statue": 'success', 'data': '点过赞了', 'judgement': False}, safe=False)
                    else:
                        return JsonResponse({"statue": 'success', 'data': '没有点过赞', 'judgement': True}, safe=False)
                except:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''给文章点赞'''

    def post(self, request):
        try:
            user_id = request.POST.get('user_id')
            choice_classfiy = request.POST.get('choice_classfiy')
            type_id = request.POST.get('type_id')
            query_data = Article.objects.get(id=type_id)
            try:
                ZanCount.objects.create(user_id=user_id, choice_classfiy=choice_classfiy, type_id=type_id)
                z = query_data.zanc
                c_z = 1 + int(z)
                query_data.zanc = c_z
                query_data.save()
            except:
                return JsonResponse({"statue": 'false', 'msg': '你不能再点了,你关注过了'}, safe=False)
            return JsonResponse({"statue": 'success', 'msg': '成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HouseCommentView(View):
    '''楼盘评论列表页'''

    def get(self, request):
        try:
            build_id = request.GET.get('only_id')
            ur = request.GET.get('user_id')
            query_data = Comment.objects.values('id', 'create_time', 'catgrage_id', 'click_count', 'village_id',
                                                'content', 'head_img', 'author_name', 'author_id').filter(
                Q(village_id=build_id) & Q(catgrage_id='')).order_by('-create_time')
            query_list = list(query_data)
            paginator = Paginator(query_list, 5)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for a in page_value:
                json_dict = {}
                cid = a['id']
                zan = ZanCount.objects.filter(Q(type_id=cid) & Q(user_id=ur) & Q(choice_classfiy=0)).count()
                json_dict['zan_num'] = int(zan)
                qd = Comment.objects.filter(catgrage_id=cid).values('id', 'catgrage_id', 'create_time', 'click_count',
                                                                    'village_id', 'content', 'head_img', 'author_name',
                                                                    'author_id').order_by('-create_time')
                qd_list = list(qd)
                newqd = []
                for kk in qd_list:
                    z = {}
                    qd_id = kk['id']
                    zan1 = ZanCount.objects.filter(Q(type_id=qd_id) & Q(user_id=ur) & Q(choice_classfiy=0)).count()
                    z['zan_num1'] = int(zan1)
                    z['catgrage_id'] = kk['catgrage_id']
                    z['create_time'] = kk['create_time']
                    z['click_count'] = kk['click_count']
                    z['village_id'] = kk['village_id']
                    z['content'] = kk['content']
                    z['head_img'] = kk['head_img']
                    z['author_name'] = kk['author_name']
                    z['author_id'] = kk['author_id']
                    newqd.append(z)
                json_dict['id'] = a['id']
                json_dict['create_time'] = a['create_time']
                json_dict['catgrage_id'] = a['catgrage_id']
                json_dict['click_count'] = a['click_count']
                json_dict['village_id'] = a['village_id']
                json_dict['content'] = a['content']
                json_dict['head_img'] = a['head_img']
                json_dict['content'] = a['content']
                json_dict['author_name'] = a['author_name']
                json_dict['author_id'] = a['author_id']
                json_dict['answer'] = newqd
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''给文章取消赞'''

    def post(self, request):
        try:
            user_id = request.POST.get('user_id')
            type_id = request.POST.get('artical_id')
            try:
                ZanCount.objects.filter(Q(user_id=user_id) & Q(type_id=type_id) & Q(choice_classfiy=1)).delete()
            except:
                return JsonResponse({"statue": 'false', 'msg': '取消点赞成功'}, safe=False)
            return JsonResponse({"statue": 'success', 'msg': '成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MoreAdviserView(View):
    '''楼盘评论更多'''

    def get(self, request):
        try:
            building_id = request.GET.get('only_id')  # 评论id
            query_data = Comment.objects.values().filter(village_id=building_id).order_by('-create_time')
            query_list = list(query_data)

            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['click_count'] = i['click_count']
                json_dict['author_name'] = i['author_name']
                json_dict['author_id'] = i['author_id']
                json_dict['village_id'] = i['village_id']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['head_img'] = i['head_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    # 我要评论
    def post(self, request):
        try:
            catgrage = request.POST.get('catgrage_id')  # 属于那个评论默认为 空 ''
            building_id = request.POST.get('village_id')  # 楼盘id
            author_name = request.POST.get('author_name')  # 作者名称
            author_id = request.POST.get('author_id')  # 作者id
            title = request.POST.get('title')  # 标题
            content = request.POST.get('content')  # 内容
            head_img = request.POST.get('img')

            if catgrage != '':
                # bd = BuildingDetial.objects.get(id=building_id)
                fid = request.POST.get('father_id')
                pass
                # mp = MiddleUnionId.objects.get(id=fid)
                # tim = datetime.datetime.now()
                # to_user, build, time, answer
                # kanfanghuifuxiaoxituisong(mp.gong_open_id, bd.building_name,tim, content)
            else:
                pass

            Comment.objects.create(catgrage_id=catgrage,
                                   author_name=author_name,
                                   village_id=building_id,
                                   title=title,
                                   content=content,
                                   author_id=author_id,
                                   head_img=head_img
                                   )

            return JsonResponse({"STATUE": 'success', 'DATA': '发表成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class GiveCommentAdviserView(View):
    '''给评论取消赞'''

    def get(self, request):
        try:
            only_id = request.GET.get('only_id')  # 那条评论id
            user_id = request.GET.get('user_id')  # 用户id
            query_data = Comment.objects.get(id=only_id)
            count = ZanCount.objects.filter(Q(type_id=only_id) & Q(user_id=user_id) & Q(choice_classfiy=0)).count()
            if count == 0:
                return JsonResponse({"statue": 'false', 'msg': '你没点过赞, 不能取消'}, safe=False)
            elif count == 1:
                try:
                    ZanCount.objects.filter(Q(type_id=only_id) & Q(user_id=user_id)).delete()
                    z = query_data.click_count
                    c_z = int(z) - 1
                    query_data.click_count = c_z
                    query_data.save()
                    return JsonResponse({"statue": 'success', 'msg': '取消成功'}, safe=False)
                except:
                    return JsonResponse({"statue": 'false', 'msg': '删除失败'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''给评论点赞'''

    def post(self, request):
        try:
            only_id = request.POST.get('only_id')
            user_id = request.POST.get('user_id')
            num = request.POST.get('zan')
            choice_classfiy = request.POST.get('choice_classfiy')
            type_id = request.POST.get('type_id')
            query_data = Comment.objects.get(id=type_id)

            count = ZanCount.objects.filter(Q(type_id=only_id) & Q(user_id=user_id) & Q(choice_classfiy=0)).count()
            if count == 0:
                try:
                    ZanCount.objects.create(user_id=user_id, choice_classfiy=choice_classfiy, type_id=type_id)
                    z = query_data.click_count
                    c_z = 1 + int(z)
                    query_data.click_count = c_z
                    query_data.save()
                    return JsonResponse({"statue": 'success', 'msg': '成功'}, safe=False)
                except:
                    return JsonResponse({"statue": 'false', 'msg': '你不能再点了,你关注过了'}, safe=False)
            elif count == 1:
                return JsonResponse({"statue": 'false', 'msg': '点过了, 不能再点'}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ClickCommentView(View):
    '''楼盘评论之点评'''

    def get(self, request):
        try:
            catgrage = request.GET.get('catgrage_id')  # 属于那个评论id
            building_id = request.GET.get('only_id')  # 楼盘id

            query_data = Comment.objects.filter(Q(catgrage_id=catgrage) & Q(village_id=building_id)).values(
                'id', 'create_time', 'content', 'author_name', 'head_img').order_by('-create_time')
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 5)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['content'] = i['content']
                json_dict['author_name'] = i['author_name']
                json_dict['head_img'] = i['head_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    # 评论详情页
    def post(self, request):
        try:
            cd = request.POST.get('comment_id')  # 属于那个评论id
            query_data = Comment.objects.filter(id=cd).values('id', 'create_time', 'content', 'author_name', 'head_img',
                                                              'click_count').order_by('-create_time')
            count = Comment.objects.filter(catgrage_id=cd).count()
            query_list = query_data[0]
            data_list = []
            json_dict = {}
            json_dict['id'] = query_list['id']
            json_dict['create_time'] = query_list['create_time']
            json_dict['content'] = query_list['content']
            json_dict['author_name'] = query_list['author_name']
            json_dict['head_img'] = query_list['head_img']
            json_dict['click_count'] = query_list['click_count']
            json_dict['answer_count'] = count
            data_list.append(json_dict)
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HousePurchaseInformationPageView(View):
    '''购房资料七个组件/摇号常见问题/公积金问题/征信打印指南/资料模板下载/资格查询/摇号流程/'''

    def get(self, request):
        try:
            req = request.GET.get('ch_id')
            data = QuestionEveryProblem.objects.values().filter(choice=req)
            query_list = list(data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['create_time'] = i['create_time']
                json_dict['img'] = i['img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class RimVillageView(View):
    '''周边楼盘'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = BuildingDetial.objects.values().filter(id=req)
            query_list = list(query_data)
            n_list = []
            for n in query_list:
                number = n['land_id']
                name = BuildingDetial.objects.values().filter(land_id=number)
                n_list.append(name)
            paginator = Paginator(n_list[0], 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']
                json_dict['building_name'] = i['building_name']
                json_dict['only_id'] = i['id']
                json_dict['building_create_time'] = i['building_create_time']
                json_dict['attention_degree'] = i['attention_degree']
                json_dict['comment_count'] = i['comment_count']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['unit_price'] = i['unit_price']

                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"Statue": 'success', 'Data': data_list, 'Count': total_page}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SamePriceVillageView(View):
    '''同价位楼盘'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = BuildingDetial.objects.values().filter(id=req)
            query_list = list(query_data)
            n_list = []
            for n in query_list:
                money = int(n['unit_price'])
                start_money = str(money - 5000)
                end_money = str(money + 5000)
                money_data = BuildingDetial.objects.values().filter(unit_price__gte=start_money).filter(
                    unit_price__lte=end_money)
                n_list.append(money_data)
            paginator = Paginator(n_list[0], 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['land_id']
                query_other_data = LandDistrict.objects.values().get(id=a)
                json_dict['land_id'] = query_other_data['name']
                json_dict['building_name'] = i['building_name']
                json_dict['only_id'] = i['id']
                json_dict['building_create_time'] = i['building_create_time']
                json_dict['attention_degree'] = i['attention_degree']
                json_dict['comment_count'] = i['comment_count']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['unit_price'] = i['unit_price']
                build_id = i['id']
                im = BuildingImage.objects.filter(fk_id=build_id).values('photo_image')
                im_list = list(im)
                for aaa in im_list:
                    json_dict['img'] = aaa
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"Statue": 'success', 'Data': data_list, 'Count': total_page}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class MapHouseView(View):
    '''地图找房'''

    def get(self, request):
        try:
            map = request.GET.get('map')
            if map != '地图找房':
                return JsonResponse({'Code': 400, 'Errmsg': '参数错误'})
            lad = LandDistrict.objects.all().values('id', 'name', 'key_name')
            ladlist = list(lad)
            data_list = []
            for aaa in ladlist:
                json_dict = {}
                iid = aaa['id']
                data = BuildingDetial.objects.filter(land_id=iid).values('id', 'longitude', 'latitude', 'building_name',
                                                                         'land_id')
                query_list = list(data)
                json_dict['id'] = aaa['id']
                json_dict['name'] = aaa['name']
                json_dict['key_name'] = aaa['key_name']
                # json_dict['data'] = query_list
                c = []
                for bbb in query_list:
                    t = {}
                    t['id'] = bbb['id']
                    t['latitude'] = bbb['latitude']
                    t['longitude'] = bbb['longitude']
                    t['iconPath'] = 'none'
                    t['callout'] = {
                        'content': bbb['building_name'],
                        'color': '#333',
                        'fontSize': 14,
                        'borderWidth': 1,
                        'borderRadius': 10,
                        'borderColor': '#000000',
                        'bgColor': '#fff',
                        'padding': 5,
                        'display': 'ALWAYS',
                        'textAlign': 'center'
                    }
                    c.append(t)
                json_dict['data'] = c
                data_list.append(json_dict)
                if ladlist == []:
                    return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"Statue": 'success', 'Data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class TranFindHouseView(View):
    '''地铁找房'''

    def get(self, request):
        try:
            req = request.GET.get('sub_id')
            req_data = BuildingDetial.objects.values().filter(train__subway__id=req)
            query_list = list(req_data)
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['only_id'] = i['id']

                a = i['id']
                p = BuildingImage.objects.filter(fk_id=a).values('photo_image')
                d = i['land_id']
                pp = LandDistrict.objects.filter(id=d).values('name')
                json_dict['land'] = pp[0]['name']
                json_dict['photo_image'] = p[0]['photo_image']
                json_dict['building_name'] = i['building_name']
                json_dict['unit_price'] = i['unit_price']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['comment_count'] = i['comment_count']
                json_dict['longitude'] = i['longitude']
                json_dict['latitude'] = i['latitude']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'False', 'Msg': 'not_found'})
            return JsonResponse({"Statue": 'success', 'Data': data_list, 'Count': total_page}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SurroundingFacilityLocationView(View):
    '''周边配套地块附近新房入库'''

    def get(self, request):
        pass

    '''周边配套经纬度入库'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body())
            bd = json_dict.get('bd_id')
            pt = json_dict.get('query')
            lc = json_dict.get('location')
            del json_dict['bd_id']
            del json_dict['query']
            del json_dict['location']
            data = surrounding_facility(pt, lc)
            try:
                BuildingDetial.objects.filter(id=bd).update(**json_dict)
            except:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            return JsonResponse({"Statue": 'success', 'Data': data}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class LongLatCreateView(View):
    '''楼盘经纬度入库'''

    def get(self, request):
        try:
            bd = request.GET.get('only_id')
            build = BuildingDetial.objects.get(id=bd)
            ld = build.land_id
            land = LandDistrict.objects.get(id=ld)
            if build.longitude == '':
                position = '杭州市' + land.name + build.building_name
                pd = getlnglat(position)
                BuildingDetial.objects.filter(id=bd).update(longitude=pd['lng'], latitude=pd['lat'])
                return JsonResponse({'Statue': 200, 'Msg': '经查询, 你的经纬度没有, 直接调用百度地图入库了经纬度, 谢谢', 'position': pd})
            else:
                lng = build.longitude
                lat = build.latitude
                position = {'lng': lng, 'lat': lat}
                return JsonResponse({"statue": 'success', 'data': position}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''周边配套'''

    def post(self, request):
        try:
            jd = json.loads(request.body.decode('utf-8'))
            bd = jd.get('only_id')  # 楼盘id
            del jd['only_id']
            value = jd.get('data')  # train_traffic bus_site school bank catering hospital shopping park
            reqa = BuildingDetial.objects.filter(id=bd).values(value)
            req = list(reqa)
            bdn = BuildingDetial.objects.get(id=bd)
            data_list = []
            for i in req:
                jso_dict = {}
                position = '杭州市' + i[value]
                pd = getlnglat(position)
                jso_dict['position'] = pd
                jso_dict['title_name'] = i[value]
                data_list.append(jso_dict)
            return JsonResponse({"statue": 200, 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


'''购房百科'''


class SearchBuyHouseHundredDepartmentView(View):
    '''购房百科搜索'''

    def get(self, request):
        try:
            data = request.GET.get('value')
            query_data = BuyHouseHundredDepartment.objects.values().filter(title__contains=data)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['classfiy_id']
                query_other_data = BuyHouseHundredDepartmentClassfiy.objects.values().get(id=a)
                json_dict['title'] = query_other_data['name']
                json_dict['only_id'] = i['id']
                json_dict['two_title'] = i['two_title']
                json_dict['text_img'] = i['text_img']
                json_dict['text'] = i['text']
                json_dict['click_zan'] = i['click_zan']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuyHouseHundredDepartmentView(View):
    '''购房百科列表(热门问题)'''
    '''/人才政策/公积金政策/落户资格查询/购房流程/贷款办理//落户指南/房产证明/社保及限购/新手引导'''

    def get(self, request):
        if request.GET.get('value') == 'hot':
            try:
                query_data = BuyHouseHundredDepartment.objects.values().all().order_by('-click_zan')
                query_list = list(query_data)
                paginator = Paginator(query_list, 5)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    a = i['classfiy_id']
                    # print(a)
                    query_other_data = BuyHouseHundredDepartmentClassfiy.objects.get(id=a)
                    json_dict['biao_ti'] = query_other_data.name
                    json_dict['id'] = i['id']
                    json_dict['two_title'] = i['two_title']
                    json_dict['title'] = i['title']
                    json_dict['text_img'] = i['text_img']
                    json_dict['text'] = i['text']
                    json_dict['click_zan'] = i['click_zan']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            except Exception as e:
                context = {"Result": 'false', 'Msg': {e}}
                return JsonResponse(context)
        else:
            context = {"Result": 'false', 'Msg': '请求错误,请输入正确参数'}
            return JsonResponse(context)


class KnowlageKnowView(View):
    '''知识百科: 人才政策/公积金政策/落户资格查询/购房流程/贷款办理/落户指南/房产证明/社保及限购/资料模板/新手引导'''

    def get(self, request):
        try:
            req = request.GET.get('value')
            query_data = BuyHouseHundredDepartment.objects.values().filter(classfiy__name__contains=req)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 5)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['only_id'] = i['id']
                json_dict['two_title'] = i['two_title']
                json_dict['text_img'] = i['text_img']
                json_dict['text'] = i['text']
                json_dict['click_zan'] = i['click_zan']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class BuyHouseHundredDepartmentDetialView(View):
    '''知识百科详情页'''

    def get(self, request):
        try:
            req = request.GET.get('id')
            query_data = BuyHouseHundredDepartment.objects.values().filter(id=req)
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['only_id'] = i['id']
                json_dict['title'] = i['title']
                json_dict['two_title'] = i['two_title']
                json_dict['text_img'] = i['text_img']
                json_dict['text'] = i['text']
                json_dict['click_zan'] = i['click_zan']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''购房百科点赞'''

    def post(self, request):
        try:
            req = request.POST.get('buy_id')
            try:
                query_data = BuyHouseHundredDepartment.objects.get(id=req)
            except:
                return JsonResponse({"statue": 'success', 'data': '没有该条文章'}, safe=False)
            c = 1 + query_data.click_zan
            query_data.click_zan = c
            query_data.save()
            return JsonResponse({"statue": 'success', 'data': '点赞成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ThreeImageView(View):
    '''公众号/服务号/买房群'''

    def get(self, request):
        try:
            req = request.GET.get('value')
            query_data = OtherImg.objects.all()
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['feedback_classfiy'] = i['feedback_classfiy']
                json_dict['buy_house_qun'] = i['buy_house_qun']
                json_dict['feedback_img'] = i['feedback_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"STATUE": 'success', 'DATA': data_list}, safe=False)
        except Exception as e:
            context = {"RESULT": 'false', 'MSG': {e}}
            return JsonResponse(context)

    '''公众号/服务号/买房群/修改'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            bd = json_dict.get('id')
            OtherImg.objects.filter(id=bd).update(**json_dict)
            return JsonResponse({"statue": 200, 'data': '修改成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ThreeImageCreateView(View):
    '''购房百科取消赞'''

    def get(self, request):
        try:
            only_id = request.GET.get('buy_id')  # 该条记录
            user_id = request.GET.get('user_id')  # 用户id
            query_data = Comment.objects.get(id=only_id)
            try:
                ZanCount.objects.filter(Q(type_id=only_id) & Q(user_id=user_id) & Q(choice_classfiy=4)).delete()
                z = query_data.click_count
                c_z = int(z) - 1
                query_data.click_count = c_z
                query_data.save()
            except:
                return JsonResponse({"statue": 'false', 'msg': '删除失败'}, safe=False)
            return JsonResponse({"statue": 'success', 'msg': '取消成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''公众号/服务号/买房群/上传'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            OtherImg.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ThreeImageDelView(View):
    '''公众号/服务号/买房群/删除'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())  # "id":[73,74,75]
            bd = json_dict.get('id')
            for i in bd:
                OtherImg.objects.filter(id=i).delete()
            return JsonResponse({"statue": 200, 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HistoryAndLotteryView(View):
    '''首页的历史摇号'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = HistoryLottery.objects.values().filter(detial_id=req)
            count = HistoryLottery.objects.values().filter(detial_id=req).count()
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                a = BuildingDetial.objects.values().get(id=req)

                json_dict['building_name'] = a['building_name']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['decorate_situation'] = i['decorate_situation']
                json_dict['house'] = i['house']
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['house_count'] = i['house_count']
                json_dict['people_count'] = i['people_count']
                json_dict['win_probability'] = i['win_probability']
                json_dict['count'] = count
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"STATUE": 'success', 'DATA': data_list}, safe=False)
        except Exception as e:
            context = {"RESULT": 'false', 'MSG': {e}}
            return JsonResponse(context)

    '''历史摇号筛选'''

    def post(self, request):
        try:
            od = request.POST.get('only_id')
            fil = HistoryLottery.objects.filter(detial_id=od).values('id', 'lottery_time', 'win_probability')
            query_list = list(fil)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['lottery_time'] = i['lottery_time']
                try:
                    ct = i['win_probability'].split(',')
                    json_dict['all_win_probability'] = ct[0]
                except:
                    json_dict['all_win_probability'] = '-'
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"STATUE": 'success', 'DATA': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HistoryAndLotteryDetialView(View):
    '''历史摇号详情页'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            position = request.GET.get('position')
            bn = request.GET.get('bn')
            vi = request.GET.get('value_id')
            query_data = HistoryLottery.objects.values().filter(Q(detial_id=req) & Q(id=vi))
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['building_name'] = bn
                json_dict['lottery_time'] = i['lottery_time']
                json_dict['win_probability'] = i['win_probability']
                json_dict['one_price'] = i['one_price']
                json_dict['all_price'] = i['all_price']
                json_dict['position'] = position
                json_dict['decorate_situation'] = i['decorate_situation']
                json_dict['house'] = i['house']
                json_dict['cool_captial_request'] = i['cool_captial_request']
                json_dict['house_count'] = i['house_count']
                json_dict['people_count'] = i['people_count']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"STATUE": 'success', 'DATA': data_list}, safe=False)
        except Exception as e:
            context = {"RESULT": 'false', 'MSG': {e}}
            return JsonResponse(context)


'''发现'''


class SearchArticalView(View):
    '''文章搜索框'''

    def get(self, request):
        try:
            data = request.GET.get('value')
            query_data = Article.objects.values().filter(title__contains=data)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['author'] = i['author']
                json_dict['create_time'] = i['create_time']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['new_img'] = i['new_img']
                json_dict['author_img'] = i['author_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ArticletVieView(View):
    '''文章详情页'''

    def get(self, request):
        try:
            data = request.GET.get('art_id')  # 最新
            query_data = Article.objects.values().filter(id=data)
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['author'] = i['author']
                json_dict['create_time'] = i['create_time']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['land'] = i['land']
                json_dict['new_img'] = i['new_img']
                json_dict['author_img'] = i['author_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class NewArticletView(View):
    '''文章/最新文章'''

    def get(self, request):
        try:
            data = request.GET.get('new')  # 最新
            if data == '最新':
                query_data = Article.objects.values().all().order_by('-create_time')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['id'] = i['id']
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['title'] = i['title']
                    json_dict['content'] = i['content']
                    json_dict['new_img'] = i['new_img']
                    json_dict['author_img'] = i['author_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Code': 400,
                                     'Errmsg': '参数错误'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class ArticleFourView(View):
    '''买房干货/楼市解读/楼市百科/房产投资'''

    def get(self, request):
        try:
            req = request.GET.get('art_id') == '买房干货0/1/2/3'
            query_data = Article.objects.values().filter(choice_classfiy=req)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['author'] = i['author']
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['title'] = i['title']
                json_dict['content'] = i['content']
                json_dict['new_img'] = i['new_img']
                json_dict['author_img'] = i['author_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class GetSoilShotSearchView(View):
    '''土拍搜索框'''

    def get(self, request):
        try:
            data = request.GET.get('land_value')
            query_data = LandAuction.objects.values().filter(land_region__contains=data)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['land_name'] = i['land_name']
                json_dict['id'] = i['id']
                json_dict['land_region'] = i['land_region']
                json_dict['deal_date'] = i['deal_date']
                json_dict['nuddle_price'] = i['nuddle_price']
                json_dict['if_residence'] = i['if_residence']
                json_dict['land_img'] = i['land_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class GetSoilShotListView(View):
    '''土拍列表页/列表首页/区域分类/住宅类型分类'''

    def get(self, request):
        try:
            if request.GET.get('value') == '列表首页':
                query_data = LandAuction.objects.values().all().order_by('-deal_date')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Statue': 'false', 'Msg': '参数错误'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    def post(self, request):
        try:
            if request.POST.get('choice') == '全选':
                land = request.POST.get('land_id')
                house = request.POST.get('house_bloon')  # 0 or 1
                query_data = LandAuction.objects.values().filter(Q(classfiy_name=land) | Q(if_residence=house))
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            if request.POST.get('choice') == '全不选':
                # land = request.POST.get('land_id')
                # house = request.POST.get('house_bloon') # 0 or 1
                query_data = LandAuction.objects.values().all().order_by('-deal_date')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            elif request.POST.get('choice') == '区域':
                land = request.POST.get('land_id')
                # house = request.POST.get('house_bloon') # 0 or 1
                query_data = LandAuction.objects.values().filter(classfiy_name=land)
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            elif request.POST.get('choice') == '用途分类':
                # land = request.POST.get('land_id')
                house = request.POST.get('house_bloon')  # 0 or 1
                query_data = LandAuction.objects.values().filter(if_residence=house)
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Statue': 'false', 'Msg': '参数错误'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class DetialShotListViewGetSoilOrderByView(View):
    '''成交排行/区域最新'''

    def get(self, request):
        try:
            if request.GET.get('value') == '成交排行':
                query_data = LandAuction.objects.values().all().order_by('-end_parice')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            elif request.GET.get('value') == '区域最新':
                query_data = LandAuction.objects.values().all().order_by('-deal_date')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['land_name'] = i['land_name']
                    json_dict['id'] = i['id']
                    json_dict['land_region'] = i['land_region']
                    json_dict['deal_date'] = i['deal_date']
                    json_dict['nuddle_price'] = i['nuddle_price']
                    json_dict['if_residence'] = i['if_residence']
                    json_dict['land_img'] = i['land_img']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Statue': 'false', 'Msg': '参数错误'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class GetSoilShotView(View):
    '''土拍详情页'''

    def get(self, request):
        try:
            req = request.GET.get('land_id')
            query_data = LandAuction.objects.values().filter(id=req)
            query_list = list(query_data)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['land_name'] = i['land_name']
                json_dict['give_area'] = i['give_area']
                json_dict['max_volume_rate'] = i['max_volume_rate']
                json_dict['if_residence'] = i['if_residence']
                json_dict['give_year'] = i['give_year']
                json_dict['start_parice'] = i['start_parice']
                json_dict['end_parice'] = i['end_parice']
                json_dict['nuddle_price'] = i['nuddle_price']
                json_dict['overflow'] = i['overflow']
                json_dict['acquisition_company'] = i['acquisition_company']
                json_dict['for_remark'] = i['for_remark']
                json_dict['land_img'] = i['land_img']
                json_dict['land_region'] = i['land_region']
                json_dict['land_position'] = i['land_position']
                json_dict['deal_all_price'] = i['deal_all_price']
                json_dict['land_use'] = i['land_use']
                json_dict['land_ask_for'] = i['land_ask_for']
                json_dict['land_number'] = i['land_number']
                json_dict['for_remark'] = i['for_remark']
                json_dict['deal_date'] = i['deal_date']
                json_dict['land_img'] = i['land_img']
                json_dict['map'] = i['map']
                json_dict['long'] = i['long']
                json_dict['late'] = i['late']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''土拍筛选查询框'''

    def post(self, request):
        try:
            jd = json.loads(request.body.decode())  # if_sale 是否出让 classfiy_name 地区 if_residence 是否住宅
            page = jd.get('page')
            # ld = jd.get('classfiy_name_id')
            del jd['page']
            # del jd['classfiy_name_id']
            query_data = LandAuction.objects.filter(**jd).values()
            query_list = list(query_data)
            paginator = Paginator(query_list, 10)
            page = int(page)
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                # a = LandDistrict.objects.get(id=ld)
                # json_dict['land_district'] = a.name
                json_dict['land_name'] = i['land_name']
                json_dict['id'] = i['id']
                json_dict['land_region'] = i['land_region']
                json_dict['deal_date'] = i['deal_date']
                json_dict['nuddle_price'] = i['nuddle_price']
                json_dict['if_residence'] = i['if_residence']
                json_dict['land_img'] = i['land_img']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SharingSearchView(View):
    '''分享堂搜索框'''

    def get(self, request):
        try:
            data = request.GET.get('land_value')  # 楼盘名称
            req_data = BuildingDetial.objects.values().filter(building_name__contains=data)
            for t in req_data:
                share_id = t['id']
                query_data = Share.objects.values().filter(bd_id=share_id)
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['id'] = i['id']
                    json_dict['middle_fk_id'] = i['middle_fk_id']
                    json_dict['bd_id'] = i['bd_id']
                    json_dict['building_name'] = i['building_name']
                    json_dict['mobile'] = i['mobile']
                    json_dict['author'] = i['author']
                    json_dict['content'] = i['content']
                    json_dict['browse_count'] = i['browse_count']  # 上传入楼盘浏览量高的
                    json_dict['img'] = i['img']
                    json_dict['video'] = i['video']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''分享堂筛选查询'''

    def post(self, request):
        try:
            choice = request.POST.get('hot_new')  # 最热
            query_data = Share.objects.all().order_by('-browse_count')
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.POST.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['middle_fk_id'] = i['middle_fk_id']
                json_dict['bd_id'] = i['bd_id']
                json_dict['building_name'] = i['building_name']
                json_dict['mobile'] = i['mobile']
                json_dict['author'] = i['author']
                json_dict['content'] = i['content']
                json_dict['browse_count'] = i['browse_count']  # 上传入楼盘浏览量高的
                json_dict['img'] = i['img']
                json_dict['video'] = i['video']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class SharingSearchListView(View):
    '''分享堂列表页'''

    def get(self, request):
        try:
            cho = request.GET.get('choice')  # 0,1,2,3
            # cla = request.GET.get('classfiy') # 公寓, 住宅
            ur = request.GET.get('ur_id')  # 使用者id
            if cho == '0':
                query_data = Share.objects.all().values().order_by('-create_time')
                query_list = list(query_data)
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['id'] = i['id']
                    json_dict['middle_fk_id'] = i['middle_fk_id']
                    json_dict['bd_id'] = i['bd_id']
                    json_dict['building_name'] = i['building_name']
                    json_dict['mobile'] = i['mobile']
                    json_dict['author'] = i['author']
                    json_dict['content'] = i['content']
                    json_dict['browse_count'] = i['browse_count']  # 上传入楼盘浏览量高的
                    json_dict['img'] = i['img']
                    json_dict['video'] = i['video']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            elif cho == '3':
                req = AttentionVillage.objects.filter(user_id=ur).values('building_id')
                for k in req:
                    kk = k['building_id']
                    query_data = Share.objects.filter(bd_id=kk).values().order_by('-create_time')
                    query_list = list(query_data)
                    print(query_list)
                    # 分页
                    paginator = Paginator(query_list, 10)
                    page = int(request.GET.get('page'))
                    try:
                        page_value = paginator.page(page)
                    except EmptyPage:
                        return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                    total_page = paginator.num_pages
                    data_list = []
                    for i in page_value:
                        json_dict = {}
                        json_dict['id'] = i['id']
                        json_dict['middle_fk_id'] = i['middle_fk_id']
                        json_dict['bd_id'] = i['bd_id']
                        json_dict['building_name'] = i['building_name']
                        json_dict['mobile'] = i['mobile']
                        json_dict['author'] = i['author']
                        json_dict['content'] = i['content']
                        json_dict['browse_count'] = i['browse_count']  # 上传入楼盘浏览量高的
                        json_dict['img'] = i['img']
                        json_dict['video'] = i['video']
                        json_dict['create_time'] = i['create_time']
                        data_list.append(json_dict)
                    if query_list == []:
                        return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                    return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            else:
                red = Share.objects.filter(choice_classfiy=cho).values().order_by('-create_time')
                query_list = list(red)
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['id'] = i['id']
                    json_dict['middle_fk_id'] = i['middle_fk_id']
                    json_dict['bd_id'] = i['bd_id']
                    json_dict['building_name'] = i['building_name']
                    json_dict['mobile'] = i['mobile']
                    json_dict['author'] = i['author']
                    json_dict['content'] = i['content']
                    json_dict['browse_count'] = i['browse_count']  # 上传入楼盘浏览量高的
                    json_dict['img'] = i['img']
                    json_dict['video'] = i['video']
                    json_dict['create_time'] = i['create_time']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''发布分享堂'''

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            Share.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '发布成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerTypeOrderView(View):
    '''默认排序'''

    def get(self, request):
        try:
            if request.GET.get('order_by') == '浏览量':
                query_data = Question.objects.values().all().order_by('-browse_count')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['img'] = '微信头像'
                    json_dict['title'] = i['title']
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['answer_count'] = i['answer_count']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['buy_house_status'] = i['buy_house_status']
                    json_dict['tou_choice'] = i['tou_choice']
                    json_dict['buy_sale_choice'] = i['buy_sale_choice']
                    json_dict['decoration_choice'] = i['decoration_choice']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            elif request.GET.get('order_by') == '创建时间':
                query_data = Question.objects.values().all().order_by('-create_time')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['img'] = '微信头像'
                    json_dict['title'] = i['title']
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['answer_count'] = i['answer_count']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['buy_house_status'] = i['buy_house_status']
                    json_dict['tou_choice'] = i['tou_choice']
                    json_dict['buy_sale_choice'] = i['buy_sale_choice']
                    json_dict['decoration_choice'] = i['decoration_choice']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerView(View):
    '''问答列表首页'''

    def get(self, request):
        try:
            if request.GET.get('value') == '问答':
                # start 开始修改
                query_data = Question.objects.values().all().order_by('create_time')
                # end   开始结束
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.GET.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['author'] = i['author']
                    json_dict['id'] = i['id']
                    json_dict['create_time'] = i['create_time']
                    json_dict['img'] = '微信头像'
                    json_dict['title'] = i['title']
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['answer_count'] = i['answer_count']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['buy_house_status'] = i['buy_house_status']
                    json_dict['tou_choice'] = i['tou_choice']
                    json_dict['buy_sale_choice'] = i['buy_sale_choice']
                    json_dict['decoration_choice'] = i['decoration_choice']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            else:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    def post(self, request):
        try:
            a = request.POST.get('a')  # 0,1,2,3
            b = request.POST.get('b')  # 0,1,2
            c = request.POST.get('c')  # 0,1,2
            # d = request.POST.get('d') # 0,1

            qa_cla = {key: value for key, value in
                      zip(['buy_house_status', 'tou_choice', 'buy_sale_choice', 'decoration_choice'],
                          [int(i) for i in a.split(',')]) if value != 0}
            if b is not None and b != '0':
                qa_cla['choice_classfiy'] = int(b)
            if c == '0':
                query_data = Question.objects.filter(**qa_cla).values()
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['id'] = i['id']
                    json_dict['img'] = '微信头像'
                    json_dict['title'] = i['title']
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['answer_count'] = i['answer_count']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['buy_house_status'] = i['buy_house_status']
                    json_dict['tou_choice'] = i['tou_choice']
                    json_dict['buy_sale_choice'] = i['buy_sale_choice']
                    json_dict['decoration_choice'] = i['decoration_choice']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            elif c == '1':
                query_data = Question.objects.filter(**qa_cla).values().order_by(
                    '-browse_count')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['id'] = i['id']
                    json_dict['img'] = '微信头像'
                    json_dict['title'] = i['title']
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['answer_count'] = i['answer_count']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['buy_house_status'] = i['buy_house_status']
                    json_dict['tou_choice'] = i['tou_choice']
                    json_dict['buy_sale_choice'] = i['buy_sale_choice']
                    json_dict['decoration_choice'] = i['decoration_choice']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            elif c == '2':
                query_data = Question.objects.filter(**qa_cla).values().order_by('-create_time')
                query_list = list(query_data)
                # 分页
                paginator = Paginator(query_list, 10)
                page = int(request.POST.get('page'))
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400,
                                         'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['author'] = i['author']
                    json_dict['create_time'] = i['create_time']
                    json_dict['id'] = i['id']
                    json_dict['img'] = '微信头像'
                    json_dict['title'] = i['title']
                    json_dict['choice_classfiy'] = i['choice_classfiy']
                    json_dict['answer_count'] = i['answer_count']
                    json_dict['browse_count'] = i['browse_count']
                    json_dict['buy_house_status'] = i['buy_house_status']
                    json_dict['tou_choice'] = i['tou_choice']
                    json_dict['buy_sale_choice'] = i['buy_sale_choice']
                    json_dict['decoration_choice'] = i['decoration_choice']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)

            else:
                return JsonResponse({'Msg': 'bad request'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerSearchView(View):
    '''问答搜索框'''

    def get(self, request):
        try:
            req = request.GET.get('value')
            query_data = Question.objects.values().filter(title__contains=req)
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                json_dict['author'] = i['author']
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['img'] = '微信头像'
                json_dict['title'] = i['title']
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['answer_count'] = i['answer_count']
                json_dict['browse_count'] = i['browse_count']
                json_dict['buy_house_status'] = i['buy_house_status']
                json_dict['tou_choice'] = i['tou_choice']
                json_dict['buy_sale_choice'] = i['buy_sale_choice']
                json_dict['decoration_choice'] = i['decoration_choice']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class QuestionAnswerDetialView(View):
    '''问答详情页/提问'''

    def get(self, request):
        try:
            id = request.GET.get('id')  # 问题的id

            # start 开始修改
            question = Question.objects.get(id=id)
            question.browse_count += 1
            question.save()
            # end   结束修改

            query_data = Question.objects.filter(id=id).values()
            question_list = list(query_data)

            data_list = []
            for i in question_list:
                json_dict1 = {}
                json_dict1['id'] = i['id']
                json_dict1['choice_classfiy'] = i['choice_classfiy']
                json_dict1['buy_house_status'] = i['buy_house_status']
                json_dict1['title'] = i['title']
                json_dict1['author'] = i['author']
                json_dict1['author_id'] = i['author_id']
                json_dict1['create_time'] = i['create_time']
                json_dict1['tou_choice'] = i['tou_choice']
                json_dict1['buy_sale_choice'] = i['buy_sale_choice']
                json_dict1['decoration_choice'] = i['decoration_choice']
                json_dict1['q_type'] = i['q_type']
                json_dict1['content'] = i['content']
                json_dict1['browse_count'] = i['browse_count']
                json_dict1['answer_count'] = i['answer_count']
                json_dict1['head_img'] = i['head_img']
                data_list.append(json_dict1)
            if question_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'question_data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IWantToAnswerView(View):
    '''问答详情页/回答'''

    def get(self, request):
        try:
            qd = request.GET.get('question_id')
            ur = request.GET.get('user_id')
            query_data = Answer.objects.filter(question_id=qd).values('id', 'content', 'aut', 'create_time',
                                                                      'click_count', 'head_img').order_by(
                '-create_time')
            query_list = list(query_data)
            paginator = Paginator(query_list, 5)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['id']
                zc = ZanCount.objects.filter(Q(choice_classfiy=2) & Q(user_id=ur) & Q(type_id=a)).count()
                json_dict['zan_num'] = zc
                d = Answer.objects.filter(Q(catgrage_id=a) & Q(question_id=qd)).values('id', 'content', 'aut',
                                                                                       'create_time', 'click_count',
                                                                                       'head_img')
                dd = list(d)
                json_dict['id'] = i['id']
                json_dict['create_time'] = i['create_time']
                json_dict['content'] = i['content']
                json_dict['aut'] = i['aut']
                json_dict['click_count'] = i['click_count']
                json_dict['head_img'] = i['head_img']
                json_dict['comment'] = dd
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''问答/我要回答'''

    def post(self, request):
        try:
            # start 开始修改
            mp_id = request.POST.get('mp_id')  # 顾问id
            question = request.POST.get('question_id')  # 问题 id
            content = request.POST.get('content')  # 内容
            aut = request.POST.get('aut')  # 作者名
            head_img = request.POST.get('head_img')  # 头像
            catgrage_id = request.POST.get('catgrage_id')  # 没有传空

            Answer.objects.create(question_id=question, com=question, content=content, aut=aut, aut_id=mp_id,
                                  head_img=head_img, catgrage_id=catgrage_id)

            question = Question.objects.get(id=question)
            question.answer_count += 1
            question.choice_classfiy = 1
            question.save()
            # end   结束修改

            return JsonResponse({"statue": 'success', 'data': '回答成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class DeleteAnswerAndZanView(View):
    '''删除回答'''

    def get(self, request):
        try:
            req = request.GET.get('answer_id')
            Answer.objects.filter(id=req).delete()
            return JsonResponse({"statue": 'success', 'data': '删除成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''回答点赞'''

    def post(self, request):
        try:
            only_id = request.POST.get('only_id')  # 点赞的回答id(查询点赞量用)
            user_id = request.POST.get('user_id')  # 用户id
            num = request.POST.get('zan')  # 1
            choice_classfiy = request.POST.get('choice_classfiy')  # 2
            type_id = request.POST.get('type_id')  # 当前评论的id
            query_data = Answer.objects.get(id=only_id)
            cou = ZanCount.objects.filter(Q(user_id=user_id) & Q(type_id=only_id)).count()
            if cou == 0:
                try:
                    ZanCount.objects.create(user_id=user_id, choice_classfiy=2, type_id=type_id)
                    z = query_data.click_count
                    c_z = 1 + int(z)
                    query_data.click_count = c_z
                    query_data.save()
                    return JsonResponse({"statue": 'success', 'msg': '成功'}, safe=False)
                except:
                    return JsonResponse({"statue": 'false', 'msg': '你不能再点了,你关注过了'}, safe=False)
            else:
                return JsonResponse({"statue": 'success', 'msg': '失败'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class GiveAnswerDisZanView(View):
    '''给回答取消赞'''

    def post(self, request):
        try:
            only_id = request.POST.get('only_id')  # 当前评论的id
            user_id = request.POST.get('user_id')  # 用户id
            query_data = Answer.objects.get(id=only_id)
            count = ZanCount.objects.filter(user_id=user_id, choice_classfiy=2, type_id=only_id).count()
            if count == 0:
                return JsonResponse({"statue": 'false', 'msg': '删除失败, 你并没有点赞额?'}, safe=False)
            else:
                try:
                    ZanCount.objects.filter(Q(type_id=only_id) & Q(user_id=user_id) & Q(choice_classfiy=2)).delete()
                    z = query_data.click_count
                    c_z = int(z) - 1
                    query_data.click_count = c_z
                    query_data.save()
                    return JsonResponse({"statue": 'success', 'msg': '取消成功'}, safe=False)
                except:
                    return JsonResponse({"statue": 'false', 'msg': '删除失败'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class IWantToQuestionView(View):
    '''我要提问'''

    def post(self, request):
        try:
            type1 = request.POST.get('type1')  # 购房资格
            type2 = request.POST.get('type2')  # 投资指南
            type3 = request.POST.get('type3')  # 买房卖房
            # type4 = request.POST.get('type4') # 装修

            content = request.POST.get('content')
            id_id = request.POST.get('id')
            name = request.POST.get('name')

            Question.objects.create(
                name_id=id_id,
                author_id=id_id,
                author=name,
                title=content,
                buy_house_status=type1,
                tou_choice=type2,
                buy_sale_choice=type3,
                choice_classfiy=3
            )

            return JsonResponse({"statue": 'success', 'data': '提问成功'}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CreateSeaPaperView(View):
    '''生成问题海报'''

    def get(self, request):
        try:
            if request.GET.get('value') == '问题海报':
                req = request.GET.get('id')
                query_data = Question.objects.values().get(id=req)
                query_list = list(query_data)
                data_list = []
                for i in query_list:
                    json_dict = {}
                    json_dict['title'] = i['title']
                    json_dict['id'] = i['id']
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
            else:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''户型图分类筛选框'''

    def post(self, request):
        try:
            od = request.POST.get('only_id')
            req = HouseImage.objects.filter(fk_id=od).values('choice_classfiy').distinct()
            query_list = list(req)
            data_list = []
            for i in query_list:
                json_dict = {}
                json_dict['choice_classfiy'] = i['choice_classfiy']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"STATUE": 'success', 'DATA': data_list}, safe=False)
        except  Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AdviserView(View):
    '''置业顾问排行榜列表页'''

    def get(self, request):
        try:
            # req = request.GET.get('value')
            query_data = MiddlePeople.objects.values().all().order_by('-live_limit')
            query_list = list(query_data)
            # 分页
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = i['building_fk_id']
                d = BuildingDetial.objects.get(id=a)
                json_dict['building_name'] = d.building_name
                json_dict['really_name'] = i['really_name']
                json_dict['header_img'] = i['header_img']
                json_dict['mobile'] = i['mobile']
                json_dict['wechat_number'] = i['wechat_number']
                json_dict['click_count'] = i['click_count']
                json_dict['building_id'] = i['building_fk_id']
                json_dict['mp_id'] = i['id']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    # 昨日榜, 今日榜
    def post(self, request):
        try:
            jd = json.loads(request.body.decode('utf-8'))
            page = jd.get('page')
            del jd['page']
            req = IntegralSubsidiary.objects.values('fk_id').filter(**jd)
            mp_list = list(req)
            for t in mp_list:
                tt = t['fk_id']
                data = MiddlePeople.objects.filter(id=tt).values()
                query_list = list(data)
                paginator = Paginator(query_list, 10)
                try:
                    page_value = paginator.page(page)
                except EmptyPage:
                    return JsonResponse({'Code': 400, 'Errmsg': 'page数据出错'})
                total_page = paginator.num_pages
                data_list = []
                for i in page_value:
                    json_dict = {}
                    json_dict['mp_id'] = i['id']
                    json_dict['really_name'] = i['really_name']
                    json_dict['rank'] = i['rank']
                    json_dict['header_img'] = i['header_img']
                    json_dict['mobile'] = i['mobile']
                    json_dict['wechat_number'] = i['wechat_number']
                    json_dict['click_count'] = i['click_count']
                    json_dict['building_id'] = i['building_fk_id']
                    b = i['building_fk_id']
                    r = BuildingDetial.objects.get(id=b)
                    json_dict['building_name'] = r.building_name
                    data_list.append(json_dict)
                if query_list == []:
                    return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
                return JsonResponse({"statue": 'success', 'data': data_list, 'Count': total_page}, safe=False)
            return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HouseImageView(View):
    '''户型图'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            choice = request.GET.get('choice')  # 0, 1, 2, 3
            if request.GET.get('cho') == '10':
                query_data = HouseImage.objects.values().filter(building_id=req)
            else:
                query_data = HouseImage.objects.values().filter(Q(building_id=req) & Q(choice_classfiy=choice))
            query_list = list(query_data)
            paginator = Paginator(query_list, 10)
            page = int(request.GET.get('page'))
            try:
                page_value = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'Code': 400,
                                     'Errmsg': 'page数据出错'})
            total_page = paginator.num_pages
            data_list = []
            for i in page_value:
                json_dict = {}
                a = BuildingDetial.objects.get(id=req)
                json_dict['building_name'] = a.building_name
                json_dict['choice_classfiy'] = i['choice_classfiy']
                json_dict['image'] = i['image']
                json_dict['house_classfiy'] = i['house_classfiy']
                json_dict['house_area'] = i['house_area']
                json_dict['create_time'] = i['create_time']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''上传户型'''

    def post(self, request):
        try:
            fk_id = request.POST.get('only_id')
            house_classfiy = request.POST.get('house_classfiy')
            choice_classfiy = request.POST.get('choice_classfiy')
            house_area = request.POST.get('house_area')
            image = request.POST.get('img')

            HouseImage.objects.values().create(fk_id=fk_id, house_classfiy=house_classfiy,
                                               choice_classfiy=choice_classfiy, house_area=house_area, image=image,
                                               building_id=fk_id)
            return JsonResponse({"statue": 'success', 'data': '上传成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HouseImgView(View):
    '''相册'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = BuildingImage.objects.filter(fk_id=req).values('photo_image', 'choice_classfiy')
            data_list0 = []
            data_list1 = []
            data_list2 = []
            data_list3 = []
            data_list4 = []
            for i in query_data:
                judge = i['choice_classfiy']
                if judge == 5:
                    json_dict0 = {}
                    json_dict0['choice_classfiy'] = i['choice_classfiy']
                    json_dict0['photo_image'] = i['photo_image']
                    data_list0.append(json_dict0)
                elif judge == 1:
                    json_dict1 = {}
                    json_dict1['choice_classfiy'] = i['choice_classfiy']
                    json_dict1['photo_image'] = i['photo_image']
                    data_list1.append(json_dict1)
                elif judge == 2:
                    json_dict2 = {}
                    json_dict2['choice_classfiy'] = i['choice_classfiy']
                    json_dict2['photo_image'] = i['photo_image']
                    data_list2.append(json_dict2)
                elif judge == 3:
                    json_dict3 = {}
                    json_dict3['choice_classfiy'] = i['choice_classfiy']
                    json_dict3['photo_image'] = i['photo_image']
                    data_list3.append(json_dict3)
                elif judge == 4:
                    json_dict4 = {}
                    json_dict4['choice_classfiy'] = i['choice_classfiy']
                    json_dict4['photo_image'] = i['photo_image']
                    data_list4.append(json_dict4)
            return JsonResponse({"statue": 'success', 'data0': data_list0, 'data1': data_list1, 'data2': data_list2,
                                 'data3': data_list3, 'data4': data_list4, }, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''上传相册'''

    def post(self, request):
        try:
            fk_id = request.POST.get('only_id')
            choice_classfiy = request.POST.get('choice_classfiy')
            photo_image = request.POST.get('photo_image')
            i = str(photo_image).split(',')
            # print(i, type(i))
            for t in i:
                BuildingImage.objects.values().create(fk_id=fk_id, choice_classfiy=choice_classfiy, photo_image=t)
            return JsonResponse({"statue": 'success', 'data': '上传成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class HouseVideoView(View):
    '''视频'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = BuildingVideo.objects.values().filter(fk_id=req)
            data_list0 = []
            data_list1 = []
            data_list2 = []
            data_list3 = []
            data_list4 = []
            for i in query_data:
                judge = i['choice_classfiy']
                if judge == 0:
                    json_dict0 = {}
                    json_dict0['choice_classfiy'] = i['choice_classfiy']
                    json_dict0['video'] = i['video']
                    json_dict0['create_time'] = i['create_time']
                    data_list0.append(json_dict0)
                elif judge == 1:
                    json_dict1 = {}
                    json_dict1['choice_classfiy'] = i['choice_classfiy']
                    json_dict1['video'] = i['video']
                    json_dict1['create_time'] = i['create_time']
                    data_list1.append(json_dict1)
                elif judge == 2:
                    json_dict2 = {}
                    json_dict2['choice_classfiy'] = i['choice_classfiy']
                    json_dict2['video'] = i['video']
                    json_dict2['create_time'] = i['create_time']
                    data_list2.append(json_dict2)
                elif judge == 3:
                    json_dict3 = {}
                    json_dict3['choice_classfiy'] = i['choice_classfiy']
                    json_dict3['video'] = i['video']
                    json_dict3['create_time'] = i['create_time']
                    data_list3.append(json_dict3)
                elif judge == 4:
                    json_dict4 = {}
                    json_dict4['choice_classfiy'] = i['choice_classfiy']
                    json_dict4['video'] = i['video']
                    json_dict4['create_time'] = i['create_time']
                    data_list4.append(json_dict4)
            return JsonResponse({"statue": 'success', 'data0': data_list0, 'data1': data_list1, 'data2': data_list2,
                                 'data3': data_list3, 'data4': data_list4, }, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    '''上传视频'''

    def post(self, request):
        try:
            fk_id = request.POST.get('only_id')
            choice_classfiy = request.POST.get('choice_classfiy')
            video = request.POST.get('video_url')
            create_time = request.POST.get('create_time')

            BuildingVideo.objects.values().create(fk_id=fk_id, choice_classfiy=choice_classfiy, video=video,
                                                  create_time=create_time)
            return JsonResponse({"statue": 'success', 'data': '上传成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CalculateView(View):
    '''一房一价图页'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            query_data = BuildingOneHouseOnePriceImage.objects.filter(fk_id=req).values('photo_image', 'create_time')
            data_list = []
            for i in query_data:
                json_dict = {}
                json_dict['create_time'] = i['create_time']
                json_dict['photo_image'] = i['photo_image']
                data_list.append(json_dict)

            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class CalculateView(View):
    '''贷款计算'''

    def post(self, request):
        try:
            judgement = request.POST.get('judgement')  # 等额本息
            all_mo = request.POST.get('all_money')  # 贷款总额
            all_yea = request.POST.get('all_year')  # 贷款年限
            inter = request.POST.get('interest')  # 年化利率

            if judgement == '等额本息':
                all_money = int(all_mo)
                # 贷款年限
                all_year = int(all_yea)
                # 总期数
                all_month = all_year * 12
                # 利率
                interest = float(inter) / (12 * 100)

                data_list = []
                for i in range(1, all_month + 1):
                    # 每月还利息
                    month_huan = all_money * (interest * (1 + interest) ** all_month) / (
                            (1 + interest) ** (all_month - 1))
                    # 贷款总额
                    dai_all = all_money
                    # 每月应还本金
                    month_ben = all_money * interest * (1 + interest) ** (i - 1) / ((1 + interest) ** all_month - 1)

                    month_gong = month_huan + month_ben  # 月供
                    # 总支付利息
                    all_xi = all_month * month_gong - all_money
                    # 还款总额
                    all_money_huan = all_xi + all_money
                    # 还款年限
                    all_n = all_year
                    # 每月应还利息
                    month_xi = all_money * interest * ((1 + interest) ** all_month - (1 + interest) ** (i - 1)) / (
                            (1 + interest) ** all_month - 1)

                    # 期数
                    date = i
                    # 剩余还款总额
                    sy_huan_all_money = all_money_huan - i * month_huan
                    json_dict = {'meiyuehuankuane': round(month_gong, 2),
                                 'daikuanzonge': round(dai_all, 2),
                                 'zongzhifulixi': round(all_xi, 2),
                                 'huankuanzonge': round(all_money_huan, 2),
                                 'huankuannianxian': round(all_n, 2),
                                 'meiyuelixi': round(month_xi, 2),
                                 'meiyuebenjin': round(month_ben, 2),
                                 'shengyuhuankuanzonge': round(sy_huan_all_money, 2),
                                 'qishu': date}
                    data_list.append(json_dict)
                return JsonResponse({"statue": '200', 'data': data_list}, safe=False)

            else:
                # 贷款总额
                all_money = int(all_mo)
                # 贷款年限
                all_year = int(all_yea)
                # 总期数
                all_month = all_year * 12
                # 利率
                interest = float(inter) / (12 * 100)
                data_list = []
                for i in range(1, all_month + 1):
                    # 每月应还本金
                    month_ben = all_money / all_month
                    yghbjlj = month_ben * i  # 已归还本金累计
                    # 每月月供额(月供总额)
                    meiyueyuegonge = (all_money / all_month) + (all_money - yghbjlj) * interest
                    # 每月应还利息（月供利息）
                    meiyueyinghuanlixi = (all_money - yghbjlj) * interest
                    # 支付总利息
                    all_xi = all_month * (all_money * interest - interest * (all_money / all_month) * (
                            all_month - 1) / 2 + all_money / all_month)
                    # 贷款总额
                    am = all_money
                    # 还款总额
                    huan_all_money = all_money + all_xi
                    # 还款年限
                    ay = all_year
                    # 期数
                    date = i
                    # 剩余还款总额
                    shengyu = all_money - meiyueyuegonge

                    json_dict = {
                        'month_ben': round(month_ben, 2), 'meiyueyuegonge': round(meiyueyuegonge, 2),
                        'meiyueyinghuanlixi': round(meiyueyinghuanlixi, 2), 'all_xi': round(all_xi, 2),
                        'am': round(am, 2), 'huan_all_money': round(huan_all_money, 2), 'ay': ay, 'date': date,
                        'shengyu': round(shengyu, 2)
                    }
                    data_list.append(json_dict)
                return JsonResponse({"statue": '200', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class PrepaymentCalculationView(View):
    '''提前还款计算'''

    def get(self, request):
        try:
            ye = request.GET.get('ye')  # 贷款余额
            lv = request.GET.get('lv')  # 利率
            hk = request.GET.get('hk')  # 提前还款额
            qs = request.GET.get('qs')  # 期数 月份
            ljlx = 0  # 初始累计利息
            ljbj = 0  # 初始累计本金
            while int(ye) > 0:
                lx = int(ye) * int(lv) / 12  # 利息
                if int(ye) > int(hk):
                    bj = int(hk) - lx
                else:
                    bj = int(ye)
                ljbj = ljbj + bj
                ljlx = ljlx + lx
                ye = int(ye) - bj
                qs = int(qs) + 1
                json_dict = {}
                json_dict['month'] = str(qs)  # 期数
                json_dict['residue'] = str(ye)  # 贷款余额
                json_dict['ben_money'] = str(bj)  # 本金
                json_dict['get_money'] = str(lx)  # 利息
                json_dict['lei_money'] = str(ljbj)  # 累计本金
                json_dict['lei_get_money'] = str(ljlx)  # 累计利息
                return JsonResponse({"statue": 'success', 'data': json_dict}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    def post(self, request):
        try:
            judgement = request.POST.get('judgement')  # 等额本息
            so_money = int(request.POST.get('so_money'))  # 原还款总额
            so_year = int(request.POST.get('so_year')) * 12  # 总期数
            huan_month = int(request.POST.get('huan_month'))  # 你还了多少期
            inter = float(request.POST.get('interest')) / (12 * 100)  # 年化利率
            fuck_you = int(request.POST.get('how_many'))  # 你想换多少
            # 缩短年限就是提前还款丁算几个月的
            if judgement == '等额本息':
                data_list = []

                # -----------------------------------------------------------------------------------------------------
                month_huan = so_money * (inter * (1 + inter) ** so_year) / ((1 + inter) ** (so_year - 1))  # 每月利息
                month_ben_ = so_money * inter * (1 + inter) ** 1 / ((1 + inter) ** so_year - 1)  # 每月应还本金
                month_gong = month_huan + month_ben_
                all_xi = so_year * month_gong - so_money  # 总支付利息
                # -----------------------------------------------------------------------------------------------------
                dang_month_huan = (so_money - (month_ben_ * huan_month)) + month_gong  # 当月需还 800000 + 10606.55
                all_so_xi = huan_month * month_huan  # 之前的总利息
                all_month_ben = huan_month * month_ben_  # 之前的总本金
                shengyuqianshu = so_money - all_month_ben - fuck_you
                next_huan = shengyuqianshu * (inter * (1 + inter) ** so_year) / ((1 + inter) ** (so_year - 1))  # 次月还款利息
                next_ben = shengyuqianshu * inter * (1 + inter) ** 1 / ((1 + inter) ** so_year - 1)  # 下月应还本金
                next_gong = next_huan + next_ben
                sheng_left = all_xi - (so_year * next_gong - shengyuqianshu)  # 可节省利息左
                next_huan_right = next_gong  # 次月还款右
                shot_sheng = fuck_you / month_gong  # 年限缩短
                new_year = shot_sheng / 12
                sheng_right = all_xi - (new_year * next_huan_right - shengyuqianshu)  # 可节省利息右

                json_dict = {'dangyuexuhuankuan': round(dang_month_huan, 2),
                             'yihuanlixi': round(all_so_xi, 2),
                             'yihuanbenjin': round(all_month_ben, 2),
                             'ciyuehuankuanzuo': round(next_huan, 2),
                             'jieshenglixizuo': round(sheng_left, 2),
                             'ciyuehuankuanyou': round(next_huan_right, 2),
                             'jieshenglixiyou': round(sheng_right, 2),
                             'nianxiansuoduan': round(shot_sheng, 2)}
                data_list.append(json_dict)
                return JsonResponse({"statue": '200', 'data': data_list}, safe=False)

            elif judgement == '等额本金':
                data_list = []
                # ------------------------------------------------------------------------------
                month_ben = so_money / so_year  # 每月应还本金
                yghbjlj = month_ben * huan_month  # 已归还本金累计
                meiyueyuegonge = (so_money / so_year) + (so_money - yghbjlj) * inter  # 每月月供额(月供总额)
                meiyueyinghuanlixi = (so_money - yghbjlj) * inter  # 每月应还利息（月供利息）
                all_xi = so_year * (so_money * inter - inter * (so_money / so_year) * (
                        so_year - 1) / 2 + so_money / so_year)  # 支付总利息
                # --------------------------------------------------------------------------------
                dang_month_huan = (so_money - (month_ben * huan_month)) + meiyueyuegonge  # 当月需还款额
                all_month_ben = yghbjlj  # 之前的总本金
                all_so_xi = meiyueyinghuanlixi * huan_month  # 之前的总利息
                # 重新计算
                shengyuqian = so_money - month_ben - fuck_you
                next_month_ben = shengyuqian / so_year  # 每月应还本金
                next_huan = next_month_ben + shengyuqian * inter  # 次月应还
                sheng_left = all_xi - meiyueyinghuanlixi * (fuck_you / month_ben)  # 可节省利息左

                shot_sheng = fuck_you / month_ben

                json_dict = {
                    'dangyuexuhuankuan': round(dang_month_huan, 2),
                    'yihuanlixi': round(all_so_xi, 2),
                    'yihuanbenjin': round(all_month_ben, 2),
                    'ciyuehuankuanzuo': round(next_huan, 2),
                    'jieshenglixizuo': round(sheng_left, 2),
                    'ciyuehuankuanyou': round(meiyueyuegonge, 2),
                    'jieshenglixiyou': round(sheng_left, 2),
                    'nianxiansuoduan': round(shot_sheng, 2)
                }
                data_list.append(json_dict)
                return JsonResponse({"statue": '200', 'data': data_list}, safe=False)

        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class AllCapteo(View):
    '''总平'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            bddata = BuildingDetial.objects.filter(id=req).values('sale_stage', 'covered_tier', 'tier_condition',
                                                                  'open_house_number')
            query_list = list(bddata)
            data_list = []
            for i in query_list:
                json_dict = {}
                r = OneHouseOnePrice.objects.filter(building_detial_id=req).values('house_dong', 'house_ceng')
                for k in r:
                    json_dict['house_dong'] = k['house_dong']
                    json_dict['house_ceng'] = k['house_ceng']
                json_dict['sale_stage'] = i['sale_stage']
                json_dict['covered_tier'] = i['covered_tier']
                json_dict['tier_condition'] = i['tier_condition']
                json_dict['open_house_number'] = i['open_house_number']
                query_data = VRAerialPhotoAllPingImage.objects.filter(fuck_id=req).values('choice_classfiy',
                                                                                          'image_url')
                query_1 = list(query_data)
                for ii in query_1:
                    json_dict['choice_classfiy'] = ii['choice_classfiy']
                    json_dict['image'] = ii['image_url']
                data_list.append(json_dict)
            if query_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

    def post(self, request):
        try:
            json_dict = json.loads(request.body.decode())
            BuildingOneHouseOnePriceImage.objects.create(**json_dict)
            return JsonResponse({"statue": 200, 'data': '添加成功'}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


class UserLookBuildingView(View):
    '''用户访问楼盘记录'''

    def get(self, request):
        try:
            req = request.GET.get('only_id')
            ur = request.GET.get('user_id')
            ct = UserLoginBuildingRecord.objects.filter(Q(fk_id=ur) & Q(building_id=req)).count()
            a = BuildingDetial.objects.get(id=req)
            coo = int(a.attention_degree)
            a.attention_degree = coo + 1
            a.save()
            return JsonResponse({"statue": 'success', 'data': ct}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)


# 添加获取所有区域
class LandDistrictListView(View):
    def get(self, request):
        try:
            Land_data = LandDistrict.objects.values()
            land_list = list(Land_data)
            data_list = []
            for i in land_list:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['name'] = i['name']
                json_dict['key_name'] = i['key_name']
                data_list.append(json_dict)
            if land_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)

        # 添加获取所有地铁站


class SubwayListView(View):
    def get(self, request):
        try:
            subway_data = Subway.objects.values()
            subway_list = list(subway_data)
            data_list = []
            for i in subway_list:
                json_dict = {}
                json_dict['id'] = i['id']
                json_dict['name'] = i['name']
                json_dict['key_name'] = i['key_name']
                data_list.append(json_dict)
            if subway_list == []:
                return JsonResponse({'Statue': 'false', 'Msg': 'not_found'})
            return JsonResponse({"statue": 'success', 'data': data_list}, safe=False)
        except Exception as e:
            context = {"Result": 'false', 'Msg': {e}}
            return JsonResponse(context)
