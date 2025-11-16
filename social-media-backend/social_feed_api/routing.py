from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/feed/$', consumers.FeedConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/post/(?P<post_id>\d+)/$', consumers.PostConsumer.as_asgi()),
]
