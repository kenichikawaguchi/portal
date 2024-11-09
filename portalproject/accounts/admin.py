from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from django.contrib.auth import get_user_model
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'icon', 'introduction')
    list_display_links = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'icon', 'introduction')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name", "email", "icon", "introduction")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "password1", "password2", "email",),
            },
        ),
    )

CustomUser = get_user_model()

admin.site.register(CustomUser, CustomUserAdmin)
