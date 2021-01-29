import hashlib
import json
import xml.etree.ElementTree as ET

from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View

from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from authorization.models import Users, MiddleUnionId, Token
from utils.WXBizDataCrypt import WXBizDataCrypt
from utils.auth import access_token, c2s, get_open_gong, send_template_message
from template_message.models import AAA
from django.core import signing


class RequestEncodeEnterDatabaseView(View):
    '''小程序接收encryptedData'''
    def get(self, request):
        try:
            # app_id = 'wx3e2f018123732318'
            app_id = 'wx49eed93625eeb3ff'
            iv = request.GET.get('iv')
            encryptedData = request.GET.get('encryptedData')
            user_id = request.GET.get('user_id')
            open_id = request.GET.get('open_id')
            # sessionkey = request.session.get('session_key')
            sessionkey = request.GET.get('session_key')
            pc = WXBizDataCrypt(app_id, sessionkey)
            parse = pc.decrypt(encryptedData, iv)
            print(parse)
            union_id = parse.get('unionId')
            if MiddleUnionId.objects.filter(union_id=union_id).count() == 0:
                MiddleUnionId.objects.create(
                    fk_id=user_id,
                    small_open_id=open_id,
                    union_id=union_id,
                )
                return JsonResponse({"statue": 'success', 'msg': '创建新的连接', 'union': parse}, safe=False)
            else:
                return JsonResponse({"statue": 'success', 'msg': '用户已关联公众号', 'union': parse}, safe=False)
        except Exception as e:
            return JsonResponse({"statue": 'false', 'msg': e}, safe=False)
            

class ReciveCheckGZHView(View):
    '''验证开发者模式'''
    def get(self, request):
        try:
            token = 'tandandan777'  # your token
            signature = request.GET.get('signature')
            timestamp = request.GET.get('timestamp')
            nonce = request.GET.get('nonce')
            echostr = request.GET.get('echostr')
            return HttpResponse(echostr)
        except Exception as e:
            return JsonResponse({"statue": 'false', 'msg': e}, safe=False)
    
    '''获取公众号open_id'''
    def post(self, request):
        from utils.analysis import Analysis
        from django.utils.encoding import smart_str
        analysisObj = Analysis(smart_str(request.body))
        toWxData = analysisObj.prase(smart_str(request.body))
        print(toWxData)
        return HttpResponse(smart_str(toWxData))


class SendTemplateMessageView(View):
    '''发送模板消息'''
    def get(self, request):
        try:
            # app_id = 'wx3e2f018123732318'
            app_id = 'wx32b98899abc39751' # 公众号

            token = access_token(app_id)
            print(1, token)
            send = send_template_message(token)
            return JsonResponse({"statue": 'success', 'data': send}, safe=False)
        except Exception as e:
            return JsonResponse({"statue": 'false', 'msg': e}, safe=False)
            

class TokenGiveQianView(View):
    '''签发token'''
    def get(self, request):
        try:
            tk = request.GET.get('gtk')
            if tk != '5c9bad6ae8d8431eb3148d92f4b042e1':
                return JsonResponse({"Error": 'false', 'Msg': '校验错误, 请传入正确参数'}, safe=False)
            else:
                req = Token.objects.get(id=1).token
                ponged = signing.b64_encode(req.encode()).decode()
                query_data = signing.b64_encode(ponged.encode()).decode()
                return JsonResponse({"statue": 'success', 'data': query_data}, safe=False)
        except Exception as e:
            return JsonResponse({"statue": 'false', 'msg': str(e)}, safe=False)

    # '''校验token'''  # Y21GbGFXRnNabXBrYTNOc1ptRnFaSE5yYkdacQ
    # def post(self, request):
    #     try:
    #         # tk = request.META['TOKEN']
    #         tk = request.POST.get('TOKEN')
    #         src = signing.b64_decode(tk.encode()).decode()
    #         dat = signing.b64_decode(src.encode()).decode()
    #         # print(dat)
    #         stk = Token.objects.get(id=1).token
    #         # print(stk)
    #         if dat != stk:
    #             return JsonResponse({"Error": 'false', 'Msg': False}, safe=False)
    #         else:
    #             return JsonResponse({"Error": 'success', 'Msg': True}, safe=False)
    #     except Exception as e:
    #         return JsonResponse({"statue": 'false', 'msg': e}, safe=False)