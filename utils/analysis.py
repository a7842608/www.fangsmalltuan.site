from xml.etree import ElementTree as ET
import time
from template_message.models import AAA
from utils.auth import access_token, get_open_gong
from authorization.models import MiddleUnionId, Token

class Analysis:
    def __init__(self, xmlData):
        print("接收到的数据：" + xmlData)

    def prase(self, xmlText):
        xmlData = ET.fromstring(xmlText)
        msgType = xmlData.find("MsgType").text
        toUserName = xmlData.find("ToUserName").text
        fromUserName= xmlData.find("FromUserName").text
        
        
        if msgType == 'text':
            content = xmlData.find("Content").text

            TextMsgObj = TextMsg(toUserName, fromUserName, content)
            return TextMsgObj.structReply()

        elif msgType == 'image':
            mediaId = xmlData.find("MediaId").text
            # pass
            ImageMsgObj = ImageMsg(toUserName,fromUserName,mediaId)
            return ImageMsgObj.structReply()

        elif msgType == 'event':
            subscribe = xmlData.find("Event").text
            
            try:
                app_id = 'wx67f2afe61fee80d7'
                data = access_token(app_id)
                Token.objects.create(token=data)
                da = get_open_gong(fromUserName, data)
                union_id = da.get('unionid')
                AAA.objects.create(values=union_id)
                if union_id == None:
                    EventMsgObj = EventMsg(toUserName, fromUserName, subscribe)
                    return EventMsgObj.structReply()
                else:
                    con = MiddleUnionId.objects.filter(union_id=union_id).count()
                    AAA.objects.create(values=con)
                    if  con == 0:
                        MiddleUnionId.objects.filter(union_id=union_id, gong_open_id=fromUserName)
                        EventMsgObj = EventMsg(toUserName, fromUserName, subscribe)
                        return EventMsgObj.structReply()
                    else:
                        req = MiddleUnionId.objects.filter(union_id=union_id).update(gong_open_id=fromUserName)
                        EventMsgObj = EventMsg(toUserName, fromUserName, subscribe)
                        return EventMsgObj.structReply()
            except Exception as e:
                AAA.objects.create(values=e)



class TextMsg:
    def __init__(self,toUser,fromUser,recvMsg):
        self._toUser = toUser
        self._fromUser = fromUser
        self._recvMsg = recvMsg
        self._nowTime = int(time.time())

    def structReply(self):
        content = self._recvMsg
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{3}]]></Content>
                </xml>
                """.format(self._fromUser, self._toUser,self._nowTime,content)   #前面两个参数的顺序需要特别注意

        return text


class EventMsg:
    def __init__(self, toUser, fromUser, subscribe):
        self._toUser = toUser
        self._fromUser = fromUser
        self._nowTime = int(time.time())
        self._subscribe = subscribe

    def structReply(self):
        text = """
                <xml>
                  <ToUserName><![CDATA[{0}]]></ToUserName>
                  <FromUserName><![CDATA[{1}]]></FromUserName>
                  <CreateTime>{2}</CreateTime>
                  <MsgType><![CDATA[event]]></MsgType>
                  <Event><![CDATA[{3}]]></Event>
                </xml>
                
                """.format(self._toUser, self._fromUser, self._nowTime,self._subscribe)
        return text


class ImageMsg:
    def __init__(self,toUser,fromUser,mediaId):
        self._toUser = toUser
        self._fromUser = fromUser
        self._rediaId = mediaId
        self._nowTime = int(time.time())
        self._mediaId = mediaId

    def structReply(self):
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{3}]]></MediaId>
                </Image>
                </xml>
                """.format(self._fromUser, self._toUser,self._nowTime,self._mediaId)   #前面两个参数的顺序需要特别注意
        from template_message.models import AAA
        return text