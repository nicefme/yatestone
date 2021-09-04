from django.db.models.base import Model
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import filters

from .models import Organization, Employee, PhoneNumber, PhoneType, Moderator
from .serializers import (OrganizationSerializer,
                          OrganizationCreateSerializer,
                          EmployeeSerializer,
                          EmployeeCreateSerializer,
                          ModeratorSerializer,
                          ModeratorCreateSerializer,
                          ModeratorOrganizationSerializer)
from .permissions import (IsOwnerOrAdminOrReadOnly,
                          IsOwnerOrAdminOrModeratorOrReadOnlyForOrg,
                          IsOwnerOrAdminOrModeratorOrReadOnlyForEmp)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    #serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnlyForOrg, ]
    pagination_class = PageNumberPagination
    search_fields = [
        'name',
    #    'organizations_of_employees__second_name',
     #   'organizations_of_employees__first_name',
     #   'organizations_of_employees__patronymic',
        'organizations_of_employees__employee__phone_number'
    ]
    filter_backends = (filters.SearchFilter,)

    
    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return OrganizationCreateSerializer

        return OrganizationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
   # queryset = Employee.objects.all()
    permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnlyForEmp, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        organization_id = self.request.parser_context['kwargs'].get('organization_id')
        queryset = Employee.objects.filter(organization=organization_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return EmployeeCreateSerializer

        return EmployeeSerializer


#class ModeratorAPIView(APIView):
  #  pagination_class = PageNumberPagination
    #permission_classes = [IsOwnerOrAdminOrReadOnly, ]

   # def get(self, request, organization_id):
   #     user = request.user
   #     queryset = Moderator.objects.filter(user=user.id, organization=organization_id)
   #     ff =queryset.values_list('moderator')
   #     ss = {}
   #     for i in enumerate(ff):
   #         ss[i[0]]=i[1][0]

   #     data = {
   #             'user': user.id,
   #             'moderator': ss,
    #            'organization': organization_id,
    #        }

    #    serializer = ModeratorSerializer(data=data)
    #    serializer.is_valid(raise_exception=True)

    #    return Response(serializer.data, status=status.HTTP_200_OK)
class ModeratorViewSet(viewsets.ModelViewSet):
  #  queryset = Moderator.objects.all()
   # serializer_class = ModeratorSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        organization_id = self.request.parser_context['kwargs'].get('organization_id')
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
