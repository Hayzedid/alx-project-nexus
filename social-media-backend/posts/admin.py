from django.contrib import admin
from .models import Post, PostMedia


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content_preview', 'content_type', 'privacy_level', 'likes_count', 'comments_count', 'shares_count', 'created_at')
    list_filter = ('content_type', 'privacy_level', 'is_pinned', 'is_edited', 'created_at')
    search_fields = ('author__username', 'content')
    readonly_fields = ('likes_count', 'comments_count', 'shares_count', 'created_at', 'updated_at')
    inlines = [PostMediaInline]
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'media_type', 'order', 'created_at')
    list_filter = ('media_type', 'created_at')
    search_fields = ('post__id', 'post__author__username')
    readonly_fields = ('created_at',)

# Register your models here.
