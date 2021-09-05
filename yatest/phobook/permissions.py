from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Moderator, Organization
from .functions import moderators_lists


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_staff)


class IsOwnerOrAdminOrReadOnlyEml(BasePermission):
    def has_object_permission(self, request, view, obj):
        organization_id = (request.parser_context['kwargs'].
                           get('organization_id'))
        author = Organization.objects.get(id=organization_id).author
        return (request.method in SAFE_METHODS
                or author == request.user
                or request.user.is_staff)


class IsOwnerOrAdminOrModeratorOrReadOnlyForOrg(BasePermission):
    def has_object_permission(self, request, view, obj):
        organization_id = obj.id
        queryset = (Moderator.objects.
                    filter(organization_id=organization_id).values_list())
        moderators_list = moderators_lists(queryset)
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_staff
                or request.user.id in moderators_list)


class IsOwnerOrAdminOrModeratorOrReadOnlyForEmp(BasePermission):
    def has_object_permission(self, request, view, obj):
        organization_id = (request.parser_context['kwargs'].
                           get('organization_id'))
        author = Organization.objects.get(id=organization_id).author
        queryset = (Moderator.objects.
                    filter(organization_id=organization_id).values_list())
        moderators_list = moderators_lists(queryset)
        return (request.method in SAFE_METHODS
                or author == request.user
                or request.user.is_staff
                or request.user.id in moderators_list)
