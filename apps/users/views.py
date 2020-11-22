from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.companies.models import Company
from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(detail=True, methods=['post'])
    def add_companies(self, request, *args, **kwargs):
        user = self.get_object()
        if 'companies' in request.data:
            existing_companies = Company.get_existing_by_pk(request.data.get('companies'))
            user.add_companies(existing_companies)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_companies(self, request, *args, **kwargs):
        user = self.get_object()
        if 'companies' in request.data:
            existing_companies = Company.get_existing_by_pk(request.data.get('companies'))
            user.update_companies(existing_companies)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_companies(self, request, *args, **kwargs):
        user = self.get_object()
        if 'companies' in request.data:
            existing_companies = Company.get_existing_by_pk(request.data.get('companies'))
            user.delete_companies(existing_companies)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def clean_companies(self, request, *args, **kwargs):
        user = self.get_object()
        user.clean_companies()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
