from django.contrib import admin
from .models import Like, Comment, CommentLike, Share, Follow, PostView


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__id')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'content_preview', 'parent', 'likes_count', 'is_edited', 'created_at')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('user__username', 'content', 'post__id')
    readonly_fields = ('likes_count', 'created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'comment__id')
    readonly_fields = ('created_at',)


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'share_type', 'caption_preview', 'created_at')
    list_filter = ('share_type', 'created_at')
    search_fields = ('user__username', 'post__id', 'caption')
    readonly_fields = ('created_at',)
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption Preview'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'post', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('user__username', 'post__id', 'ip_address')
    readonly_fields = ('viewed_at',)
    
    def user_display(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    user_display.short_description = 'User'

# Register your models here.
