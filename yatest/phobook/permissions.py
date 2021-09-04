from django.db.models import query
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Moderator

class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user or request.user.is_staff

class IsOwnerOrAdminOrModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        a = self
        b = request
        c = view
        organization_id = obj.id
        queryset = Moderator.objects.filter(organization_id=organization_id).values_list()
        ss = []
        if queryset.exists():
            for i in queryset:
                ss.append(i[2])
       # ff = request.user.id in ss
       # ыы
        return request.method in SAFE_METHODS or obj.author == request.user or request.user.is_staff or request.user.id in ss
        