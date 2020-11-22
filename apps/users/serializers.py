from rest_framework import serializers

from apps.users.models import User
from apps.companies.serializers import CompanySerializer


class UserSerializer(serializers.ModelSerializer):
    # companies = CompanySerializer(many=True)

    class Meta:
        model = User
        fields = ('pk', 'password', 'username', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}, 'pk': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        if password or password != '':
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance
