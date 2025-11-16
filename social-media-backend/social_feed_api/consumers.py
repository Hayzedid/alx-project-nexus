import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from posts.models import Post
from interactions.models import Like, Comment, Follow, Share

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{self.user_id}'
        
        # Join user group for notifications
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave user group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def notification(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['notification_type'],
            'data': event['data']
        }))

    async def like_notification(self, event):
        await self.notification(event)

    async def comment_notification(self, event):
        await self.notification(event)

    async def follow_notification(self, event):
        await self.notification(event)

    async def share_notification(self, event):
        await self.notification(event)


class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.feed_group_name = 'feed'
        
        # Join feed group
        await self.channel_layer.group_add(
            self.feed_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave feed group
        await self.channel_layer.group_discard(
            self.feed_group_name,
            self.channel_name
        )

    async def new_post(self, event):
        # Send new post to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_post',
            'data': event['data']
        }))


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = f'post_{self.post_id}'
        
        # Join post group for real-time updates
        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave post group
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def post_update(self, event):
        # Send post update to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['update_type'],
            'data': event['data']
        }))

    async def like_update(self, event):
        await self.post_update(event)

    async def comment_update(self, event):
        await self.post_update(event)

    async def share_update(self, event):
        await self.post_update(event)


# Helper functions for sending real-time notifications
async def send_like_notification(user_id, like_data):
    """Send like notification to post author"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'user_{user_id}',
        {
            'type': 'like_notification',
            'notification_type': 'like',
            'data': like_data
        }
    )

async def send_comment_notification(user_id, comment_data):
    """Send comment notification to post author"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'user_{user_id}',
        {
            'type': 'comment_notification',
            'notification_type': 'comment',
            'data': comment_data
        }
    )

async def send_follow_notification(user_id, follow_data):
    """Send follow notification to user"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'user_{user_id}',
        {
            'type': 'follow_notification',
            'notification_type': 'follow',
            'data': follow_data
        }
    )

async def send_share_notification(user_id, share_data):
    """Send share notification to post author"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'user_{user_id}',
        {
            'type': 'share_notification',
            'notification_type': 'share',
            'data': share_data
        }
    )

async def broadcast_new_post(post_data):
    """Broadcast new post to all connected feed clients"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        'feed',
        {
            'type': 'new_post',
            'data': post_data
        }
    )

async def update_post_likes(post_id, like_data):
    """Update post likes for all clients viewing the post"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'post_{post_id}',
        {
            'type': 'like_update',
            'update_type': 'like_update',
            'data': like_data
        }
    )

async def update_post_comments(post_id, comment_data):
    """Update post comments for all clients viewing the post"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'post_{post_id}',
        {
            'type': 'comment_update',
            'update_type': 'comment_update',
            'data': comment_data
        }
    )

async def update_post_shares(post_id, share_data):
    """Update post shares for all clients viewing the post"""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    await channel_layer.group_send(
        f'post_{post_id}',
        {
            'type': 'share_update',
            'update_type': 'share_update',
            'data': share_data
        }
    )
