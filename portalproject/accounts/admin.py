from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
