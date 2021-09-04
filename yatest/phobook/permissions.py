from django.db.models import query
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Moderator, Organization


def moderators_lists(queryset):
    moderators_list = []
    if queryset.exists():
        for query in queryset:
            moderators_list.append(query[2])
    return moderators_list


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user or request.user.is_staff

class IsOwnerOrAdminOrModeratorOrReadOnlyForOrg(BasePermission):
    def has_object_permission(self, request, view, obj):
        organization_id = obj.id
        #organization_id = request.parser_context['kwargs'].get('organization_id')
        #author = Organization.objects.get(id=organization_id).author
        queryset = Moderator.objects.filter(organization_id=organization_id).values_list()
        moderators_list = moderators_lists(queryset)
       # moderators_list = []
       # if queryset.exists():
       #     for query in queryset:
       #         moderators_list.append(query[2])
       # b = request.method in SAFE_METHODS
       # c = obj.author == request.user
       # f_one = obj.author 
       # f_two = request.user
       # d = request.user.is_staff
       # e = request.user.id in moderators_list
       # ss
        return request.method in SAFE_METHODS or obj.author == request.user or request.user.is_staff or request.user.id in moderators_list

class IsOwnerOrAdminOrModeratorOrReadOnlyForEmp(BasePermission):
    def has_object_permission(self, request, view, obj):
        #organization_id = obj.id
        organization_id = request.parser_context['kwargs'].get('organization_id')
        author = Organization.objects.get(id=organization_id).author
        queryset = Moderator.objects.filter(organization_id=organization_id).values_list()
        moderators_list = moderators_lists(queryset)
        #if queryset.exists():
        #    for query in queryset:
       #         moderators_list.append(query[2])
       # b = request.method in SAFE_METHODS
       # c = author == request.user
       # f_one = author
       # f_two = request.user
       # d = request.user.is_staff
       ## e = request.user.id in moderators_list
       # ss
        return request.method in SAFE_METHODS or request.method == ('POST') or author == request.user or request.user.is_staff or request.user.id in moderators_list