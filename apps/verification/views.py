import random

from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from libs.yuntongxun.sms import CCP


class SmsCodeView(View):
    '''容联云'''
    def post(self, request):
        try:
            mobile = request.POST.get('mobile')
            redis_conn = get_redis_connection('sms_code')
            # sms_code = '%06d' % random.randint(0, 999999)
            sms_code = 888888
            print(sms_code)
            redis_conn.setex('sms_%s' % mobile, 300, sms_code)
            # 9. 发送短信验证码
            # 短信模板
            # CCP().send_template_sms(mobile, [sms_code, 5], 1)
            # 10. 响应结果
            return http.JsonResponse({'Code': '200',
                                      'Statue': '发送短信成功', 'Sms_code': sms_code})
        except Exception as e:
            context = {"RESULT": 'false', 'MSG': {e}}
            return JsonResponse(context)


