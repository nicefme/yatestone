from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

from .models import CustomUser



#@admin.register(CustomUser)
class CustomUserAdmin(OrigUserAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'email', 'is_active'
    )
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
#class UserAdmin(admin.ModelAdmin):
#
#    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)