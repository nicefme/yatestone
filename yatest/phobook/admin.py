from django.contrib import admin

from .models import Organization, Employee, PhoneNumber, PhoneType, Moderator



class OrganizationAdmin(admin.ModelAdmin):

    empty_value_display = '-пусто-'


class EmployeeAdmin(admin.ModelAdmin):

    empty_value_display = '-пусто-'


class PhoneTypeAdmin(admin.ModelAdmin):

    empty_value_display = '-пусто-'


class PhoneNumberAdmin(admin.ModelAdmin):

    empty_value_display = '-пусто-'


class ModeratorAdmin(admin.ModelAdmin):

    empty_value_display = '-пусто-'


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PhoneType, PhoneTypeAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Moderator, ModeratorAdmin)