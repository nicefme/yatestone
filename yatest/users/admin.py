from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

from .models import CustomUser


class CustomUserAdmin(OrigUserAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'email', 'is_active'
    )
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'


admin.site.register(CustomUser, CustomUserAdmin)
