from rest_framework import serializers

from apps.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('pk', 'name', 'trading_name', 'registered_number', 'email', 'phone')
        extra_kwargs = {'pk': {'read_only': True}}
