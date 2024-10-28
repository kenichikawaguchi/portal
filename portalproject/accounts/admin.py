from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', 'email', 'is_staff', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)
