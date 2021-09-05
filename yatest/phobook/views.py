from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Organization, Employee, Moderator
from .serializers import (OrganizationSerializer,
                          OrganizationCreateSerializer,
                          EmployeeSerializer,
                          EmployeeCreateSerializer,
                          ModeratorSerializer,
                          ModeratorCreateSerializer,
                          ModeratorOrganizationSerializer)
from .permissions import (IsOwnerOrAdminOrReadOnly,
                          IsOwnerOrAdminOrReadOnlyEml,
                          IsOwnerOrAdminOrModeratorOrReadOnlyForOrg,
                          IsOwnerOrAdminOrModeratorOrReadOnlyForEmp)
from .filters import OrganizationFilter, EmployeeFilter


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    filter_class = OrganizationFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnlyForOrg, ]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'destroy': [IsOwnerOrAdminOrReadOnly]
    }

    def get_permissions(self):
        try:
            return (permission() for permission in
                    self.permission_classes_by_action[self.action])
        except KeyError:
            return (permission() for permission in self.permission_classes)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return OrganizationCreateSerializer
        return OrganizationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    filter_class = EmployeeFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnlyForEmp, ]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'destroy': [IsOwnerOrAdminOrReadOnlyEml]
    }

    def get_permissions(self):
        try:
            return (permission() for permission in
                    self.permission_classes_by_action[self.action])
        except KeyError:
            return (permission() for permission in self.permission_classes)

    def get_queryset(self):
        organization_id = (self.request.parser_context['kwargs'].
                           get('organization_id'))
        queryset = Employee.objects.filter(organization=organization_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return EmployeeCreateSerializer
        return EmployeeSerializer


class ModeratorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdminOrReadOnly, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        organization_id = (self.request.parser_context['kwargs'].
                           get('organization_id'))
        queryset = Moderator.objects.filter(organization=organization_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return ModeratorCreateSerializer
        return ModeratorSerializer


class ModeratorAPIView(APIView):
    def get(self, request):
        user = request.user
        moderator = Moderator.objects.filter(moderator_id=user.id)
        serializer = ModeratorOrganizationSerializer(moderator, many=True)
        context = {
            'user': f'{user}',
            'moderator': serializer.data
        }
        return Response(context)
