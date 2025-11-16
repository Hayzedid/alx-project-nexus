from django.db import models
from django.conf import settings


class Post(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('mixed', 'Mixed'),
    ]

    PRIVACY_LEVELS = [
        ('public', 'Public'),
        ('followers', 'Followers Only'),
        ('private', 'Private'),
    ]

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(blank=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')
    media_url = models.URLField(blank=True, null=True)
    privacy_level = models.CharField(max_length=10, choices=PRIVACY_LEVELS, default='public')
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['privacy_level']),
            models.Index(fields=['content_type']),
            models.Index(fields=['likes_count']),
        ]


class PostMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('gif', 'GIF'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='post_media/')
    thumbnail = models.ImageField(upload_to='post_thumbnails/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for Post {self.post.id}"

    class Meta:
        db_table = 'post_media'
        ordering = ['order']
        indexes = [
            models.Index(fields=['post', 'order']),
        ]

# Create your models here.
