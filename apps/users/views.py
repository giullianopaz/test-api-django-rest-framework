from django.shortcuts import render

from rest_framework import viewsets

from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        self.serializer_class = super().get_serializer_class()
        self.serializer_class.Meta.depth = 1 if 'related' in self.request.query_params else None
        return self.serializer_class
