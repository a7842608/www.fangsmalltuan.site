import requests
import time
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from authorization.models import Users, MiddlePeople, GoldenMoney
from utils import pay


class PayOrderView(View):
    '''发起支付请求'''
    def post(self, request):
        try:
            # 用户id
            user_id = request.POST.get('user_id')
            # 充值金额
            f_price = request.POST.get("price")

            # 获取客户端ip
            client_ip, port = request.get_host().split(":")
            # 获取小程序openid
            # openid = Users.objects.get(id=user_id).openid
            o = Users.objects.filter(id=user_id).values('open_id')
            openid = o[0]['open_id']
            # 请求微信的url
            # url = configuration.order_url
            url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
            # 拿到封装好的xml数据
            price = int(f_price) * 100
            body_data = pay.get_bodyData(openid, client_ip, price)
            print(body_data)
            # 获取时间戳
            timeStamp = str(int(time.time()))
            # 请求微信接口下单
            respone = requests.post(url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
            # print(respone)
            # 回复数据为xml,将其转为字典
            content = pay.xml_to_dict(respone.content)
            # print(content)
            if content["return_code"] == 'SUCCESS':
                # 获取预支付交易会话标识
                prepay_id = content.get("prepay_id")
                # 获取随机字符串
                nonceStr = content.get("nonce_str")
                # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
                paySign = pay.get_paysign(prepay_id, timeStamp, nonceStr)
                print(paySign)
                # 封装返回给前端的数据
                data = {"prepay_id": "prepay_id="+prepay_id, "nonceStr": nonceStr, "paySign": paySign, "timeStamp": timeStamp}
                # return HttpResponse(packaging_list(data))
            # data = {'statue':'success'}
                return JsonResponse(data)
        except Exception as e:
            context = {'MSG': {e}}
            return JsonResponse(context)


class CallBackView(View):
    '''支付成功后数据库金额修改'''
    def get(self, request):
        try:
            # 用户id
            mp = request.GET.get('mp_id')
            # 充值金额
            price = request.GET.get("price")
            d = MiddlePeople.objects.filter(id=mp).values('golden_money')
            try:
                money = d[0]['golden_money']
            except :
                return JsonResponse({'STATUE':'404', 'MSG': '无法获取'})
            change = int(money) + int(price)
            MiddlePeople.objects.filter(id=mp).update(golden_money=change)
            GoldenMoney.objects.create(fk_id=mp, money_count=change, change_beacuse='充值', choice_classfiy=0)

            return JsonResponse({'STATUE':200, 'MSG': 'SUCCESS'})
        except Exception as e:
            context = {'MSG': {e}}
            return JsonResponse(context)