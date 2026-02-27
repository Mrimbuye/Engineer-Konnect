from django.contrib import admin
from .models import Discussion, Comment

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'views', 'likes', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('views', 'created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author', 'likes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'discussion__title')
    readonly_fields = ('created_at', 'updated_at')

