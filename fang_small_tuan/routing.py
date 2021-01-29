from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import chat.routing
# import autoplatform.routing
# from autoplatform import consumers
from chat import consumers


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 【channels】（第6步）添加路由配置指向应用的路由模块
    # 'websocket': AuthMiddlewareStack(  # 使用Session中间件，可以请求中session的值
    'websocket': SessionMiddlewareStack(  # 使用Session中间件，可以请求中session的值
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
    
    # "channel": ChannelNameRouter({
    #     # "service-detection": consumers.ServiceConsumer, # AsyncConsumer
    #     "service-detection": consumers.AsyncConsumer,
        
    # }),
    
})