from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.users.models import User


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True, methods=['post'])
    def add_employees(self, request, *args, **kwargs):
        company = self.get_object()
        if 'employees' in request.data:
            existing_employees = User.get_existing_by_pk(request.data.get('employees'))
            company.add_employees(existing_employees)
        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_employees(self, request, *args, **kwargs):
        company = self.get_object()
        if 'employees' in request.data:
            existing_employees = User.get_existing_by_pk(request.data.get('employees'))
            company.update_employees(existing_employees)
        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_employees(self, request, *args, **kwargs):
        company = self.get_object()
        if 'employees' in request.data:
            existing_employees = User.get_existing_by_pk(request.data.get('employees'))
            company.delete_employees(existing_employees)
        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def clean_employees(self, request, *args, **kwargs):
        company = self.get_object()
        company.clean_employees()
        serializer = self.get_serializer(company)
        return Response(serializer.data)
