from rest_framework import serializers

from apps.companies.models import Company
from apps.users.serializers import UserSerializer


class CompanySerializer(serializers.ModelSerializer):
    employees = UserSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ('pk', 'name', 'trading_name', 'registered_number', 'email', 'phone', 'employees')
        extra_kwargs = {'pk': {'read_only': True}, 'employees': {'required': False, 'read_only': True}}
