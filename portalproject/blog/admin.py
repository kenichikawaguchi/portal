from django.contrib import admin

from .models import BlogPost, Comment, Tag, Like

from markdownx.admin import MarkdownxModelAdmin


class LikeAdmin(admin.ModelAdmin):
    fields = ['user', 'blogpost', 'comment', 'created_at']
    readonly_fields = ['created_at']


class BlogPostAdmin(MarkdownxModelAdmin):
    list_display = ['user', 'title', 'is_public', 'only_friends', 'created_at']
    readonly_fields = ['created_at']


# admin.site.register(BlogPost, MarkdownxModelAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Tag)
admin.site.register(Like, LikeAdmin)
