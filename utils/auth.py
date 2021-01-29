import datetime
import json
import requests
# from utils import proxy
import fang_small_tuan.settings

from authorization.models import Users, Token
from template_message.models import AAA

# from utils.wx.code2session import code2session


def already_authorized(request):
    is_authorized = False

    if request.session.get('is_authorized'):
        is_authorized = True

    return is_authorized


def get_user(request):
    if not already_authorized(request):
        raise Exception('用户未登录')
    open_id = request.session.get('open_id')
    user = Users.objects.get(open_id=open_id)
    return user


def c2s(appid, code):
    return code2session(appid, code)


def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    # WX_APP_SECRET = '7be8a057a4f31595abab03fac1aca35d' 
    WX_APP_SECRET = 'cfaedc7742c39a6ff0d93c269d3491d0' # 小程序
    # GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    # params = 'appid=%s&secret=%s&js_code=%s&grant_tapy=authorized_code' % (appid, fang_small_tuan.settings.WX_APP_SECRET, code)
    params = 'appid=%s&secret=%s&js_code=%s&grant_tapy=authorized_code' % (appid, WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)

    return data


def access_token(appid):
    # https请求方式: GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
    # {"statue": "success", "access_token": "39_uVHJvqA89_gKulvs88pGoP6XJFLgQZtyD5gqyV5UDVNoqD2Ln6mnN2F1v33hQOmQa4YDR4PTnXCNjyWR9O9wDPmditstcDnUsiBJh1BK-4FG3Syo1m1M5O3WtHbNPAlVRMVpMXvWv-aPMpRyHWMcAGADSI"}
    # wx67f2afe61fee80d7 公众号appid
    
    #  https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
    API = 'https://api.weixin.qq.com/cgi-bin/token'
    WX_APP_SECRET = '3cbea7232ed91f95a6421b546a00e3ac' # 公众号

    params = 'grant_type=client_credential&appid=%s&secret=%s' % (appid, WX_APP_SECRET)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    token = data.get('access_token')
    # Token.objects.create(token=token, id=1)
    return token


def token_time():
    # app_id = 'wx32b98899abc39751'
    app_id = 'wx49eed93625eeb3ff' # 小程序的
    access_token = Token.objects.get(id=1)
    at = access_token.create_time
    et = datetime.datetime.now()
    sec = et - at
    if sec.seconds >= 7200:
        Token.objects.get(id=1).delete()
        t = access_token(app_id)
        return t
    else:
        return access_token


def get_open_gong(openid, access_token):
    # https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
    # https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN 
    API = 'https://api.weixin.qq.com/cgi-bin/user/info'
    params = 'access_token=%s&openid=%s&lang=zh_CN' % (access_token, openid)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    AAA.objects.create(values=openid)
    AAA.objects.create(values=access_token)
    return data


def send_template_message(access_token):
    '''模板消息推送'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)

    '''
            {{first.DATA}}
        到访时间：{{keyword1.DATA}}
        到访楼盘：{{keyword2.DATA}}
        到访客户：{{keyword3.DATA}}
        客户电话：{{keyword4.DATA}}
        客户状态：{{keyword5.DATA}}
        {{remark.DATA}}
    '''
    jd = {
           "touser":"oroeFwhxx_cdoUXXZ0seNcIyHh40",
           "template_id":"Z1uK-D4RGLaJ4FS1i2pIVcfbUzl6u4JNU7p_p-rDAzQ",
           "appid":"wx32b98899abc39751",
           "data":{
                   "first": {
                       "value":"恭喜你购买成功！",
                       "color":"#173177"
                   },
                   "keyword1":{
                       "value":"巧克力",
                       "color":"#173177"
                   },
                   "keyword2": {
                       "value":"39.8元",
                       "color":"#173177"
                   },
                   "keyword3": {
                       "value":"2014年9月22日",
                       "color":"#173177"
                   },
                   "keyword4": {
                       "value":"2014年9月22日",
                       "color":"#173177"
                   },
                   "keyword5": {
                       "value":"2014年9月22日",
                       "color":"#173177"
                   },
                   "remark":{
                       "value":"欢迎再次购买！",
                       "color":"#173177"
                   }
           }
       }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data


def yaohaojieguotongzhi(to_user, build, wsnumber, lottery_time):
    '''摇号结果通知'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token_time())

    '''
                {{first.DATA}}
        楼盘名称：{{keyword1.DATA}}
        指标类型：{{keyword2.DATA}}
        登记编号：{{keyword3.DATA}}
        摇号时间：{{keyword4.DATA}}
        {{remark.DATA}}
    '''
    jd = {
        "touser": "{}".format(to_user),
        "template_id": "J6363o-AX736J-QShxbofoSDHaNaXr_wTcxBcMcleVs",
        "appid": "wx32b98899abc39751",
        "data": {
            "first": {
                "value": "你好, 你关注的{}摇号结果已出！".format(build),
                "color": "#173177"
            },
            "keyword1": {
                "value": "{}".format(build),
                "color": "#173177"
            },
            "keyword2": {
                "value": "{}".format('指标类型'),
                "color": "#173177"
            },
            "keyword3": {
                "value": "{}".format(wsnumber),
                "color": "#173177"
            },
            "keyword4": {
                "value": "{}".format(lottery_time),
                "color": "#173177"
            },
            "remark": {
                "value": "点击详情,查看你的摇号结果,祝您好运！",
                "color": "#173177"
            }
        }
    }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data


def jifenduihuantongzhi(to_user):
    '''积分兑换通知'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token_time())

    '''
                变更类型：{{keyword1.DATA}}
            变更原因：{{keyword2.DATA}}
            变更数量：{{keyword3.DATA}}
            {{remark.DATA}}
    '''
    jd = {
        "touser": "{}".format(to_user),
        "template_id": "N9hIFRUpN7Alv3GVxV4cTbCX0zBFUYfwWM2k5s9pgyE",
        "appid": "wx32b98899abc39751",
        "data": {
            "first": {
                "value": "每日签到可兑换5积分,今日还未签到呦！",
                "color": "#173177"
            },
            "keyword1": {
                "value": "签到",
                "color": "#173177"
            },
            "keyword2": {
                "value": "未签到的顾问",
                "color": "#173177"
            },
            "keyword3": {
                "value": "5积分待兑换",
                "color": "#173177"
            },
            "remark": {
                "value": "赶紧进入小程序签到兑换5积分吧！",
                "color": "#173177"
            }
        }
    }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data


def kehuliuyantongzhi(to_user, user_name, mobile, content, time):
    '''客户留言'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token_time())

    '''
                {{first.DATA}}
        客户名称：{{keyword1.DATA}}
        客户手机：{{keyword2.DATA}}
        客户留言：{{keyword3.DATA}}
        预约时间：{{keyword4.DATA}}
        {{remark.DATA}}
    '''
    jd = {
        "touser": "{}".format(to_user),
        "template_id": "NLOYjZi_lGe0swAm9K-juZz6PbFnp5HDmYivaXWR2rU",
        "appid": "wx32b98899abc39751",
        "data": {
            "first": {
                "value": "客户留言通知",
                "color": "#173177"
            },
            "keyword1": {
                "value": "{}".format(user_name),
                "color": "#173177"
            },
            "keyword2": {
                "value": "{}".format(mobile),
                "color": "#173177"
            },
            "keyword3": {
                "value": "{}".format(content),
                "color": "#173177"
            },
            "keyword4": {
                "value": "{}".format(time),
                "color": "#173177"
            },
            "remark": {
                "value": "您有一条新的消息,请注意查收！",
                "color": "#173177"
            }
        }
    }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data


def shenhetongguo(to_user, build, content, time):
    '''审核通过提醒'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token_time())

    '''
                {{first.DATA}}
            房源信息：{{keyword1.DATA}}
            审核内容：{{keyword2.DATA}}
            通过时间：{{keyword3.DATA}}
            {{remark.DATA}}
    '''
    jd = {
        "touser": "{}".format(to_user),
        "template_id": "sLqWOStWPpSQ-0ETL0QvGCuSapTak34TM9ox110qWC4",
        "appid": "wx32b98899abc39751",
        "data": {
            "first": {
                "value": "你好,你关注的{}今日已取证".format(build),
                "color": "#173177"
            },
            "keyword1": {
                "value": "{}".format(build),
                "color": "#173177"
            },
            "keyword2": {
                "value": "{}".format(content),
                "color": "#173177"
            },
            "keyword3": {
                "value": "{}".format(time),
                "color": "#173177"
            },
            "remark": {
                "value": "点击详情,查看更多取证信息！",
                "color": "#173177"
            }
        }
    }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data


def yixiangdengjibiao(to_user, build, name, mobile):
    '''意向登记'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token_time())

    '''
                {{first.DATA}}
            登记楼盘：{{keyword1.DATA}}
            客户姓名：{{keyword2.DATA}}
            客户手机号：{{keyword3.DATA}}
            意向金金额：{{keyword4.DATA}}
            {{remark.DATA}}
    '''
    jd = {
        "touser": "{}".format(to_user),
        "template_id": "ozFYxGMAu6WhEcOvYaVl_lDBxoPUDzLsbzom5suu7m4",
        "appid": "wx32b98899abc39751",
        "data": {
            "first": {
                "value": "客户意向登记成功通知",
                "color": "#173177"
            },
            "keyword1": {
                "value": "{}".format(build),
                "color": "#173177"
            },
            "keyword2": {
                "value": "{}".format(name),
                "color": "#173177"
            },
            "keyword3": {
                "value": "{}".format(mobile),
                "color": "#173177"
            },
            "keyword4": {
                "value": "无",
                "color": "#173177"
            },
            "remark": {
                "value": "您已完成意向登记！",
                "color": "#173177"
            }
        }
    }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data


def kanfanghuifuxiaoxituisong(to_user, build, time, answer):
    '''楼盘评论消息通知'''
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token_time())

    '''
                {{first.DATA}}
            看房时间：{{keyword1.DATA}}
            回复结果：{{keyword2.DATA}}
            {{remark.DATA}}
    '''
    jd = {
        "touser": "{}".format(to_user),
        "template_id": "OPENTM401074938",
        "appid": "wx32b98899abc39751",
        "data": {
            "first": {
                "value": "您评论的{}楼盘有了新的回复~".format(build),
                "color": "#173177"
            },
            "keyword1": {
                "value": "{}".format(time),
                "color": "#173177"
            },
            "keyword2": {
                "value": "{}".format(answer),
                "color": "#173177"
            },
            "remark": {
                "value": "请进入小程序进行评论/回复吧~！",
                "color": "#173177"
            }
        }
    }
    response = requests.post(url=url, json=jd, timeout=3, verify=False)
    data = json.loads(response.text)
    print('data', data)
    return data