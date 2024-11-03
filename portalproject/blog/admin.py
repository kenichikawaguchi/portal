from django.contrib import admin

from .models import BlogPost, Comment, Tag

from markdownx.admin import MarkdownxModelAdmin


admin.site.register(BlogPost, MarkdownxModelAdmin)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Tag)
