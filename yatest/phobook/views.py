from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Organization, Employee, PhoneNumber, PhoneType
from .serializers import (OrganizationSerializer,
                          OrganizationCreateSerializer,
                          EmployeeSerializer,
                          EmployeeCreateSerializer)
from .permissions import IsOwnerOrAdminOrReadOnly


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    #serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return OrganizationCreateSerializer

        return OrganizationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly, ]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return EmployeeCreateSerializer

        return EmployeeSerializer