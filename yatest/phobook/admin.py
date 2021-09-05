from django.contrib import admin

from .models import Organization, Employee, PhoneNumber, PhoneType, Moderator


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'author'
    )
    empty_value_display = '-пусто-'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'second_name',
        'patronymic',
        'position',
        'organization'
    )
    empty_value_display = '-пусто-'


class PhoneTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type'
    )
    empty_value_display = '-пусто-'


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'employee',
        'phone_number'
    )
    empty_value_display = '-пусто-'


class ModeratorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'moderator',
        'organization'
    )
    empty_value_display = '-пусто-'


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PhoneType, PhoneTypeAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Moderator, ModeratorAdmin)
