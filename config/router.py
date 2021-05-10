from channels.auth import AuthMiddlewareStack
from django.urls import path
from todo.schemas import MyGraphqlWsConsumer
from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter({
    "websocket":AuthMiddlewareStack(URLRouter([
        path("graphql/", MyGraphqlWsConsumer.as_asgi()),
    ]))
})