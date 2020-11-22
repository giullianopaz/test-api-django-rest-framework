from rest_framework import serializers

from apps.companies.models import Company
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'password', 'username', 'email', 'first_name', 'last_name', 'companies')
        extra_kwargs = {'password': {'write_only': True}, 'pk': {'read_only': True}, 'companies': {'required': False}}
        depth = None

    def create(self, validated_data):
        password = validated_data.pop('password') if validated_data.get('password') else None
        user = User(**validated_data)
        if password and password != '':
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.pop('password') if validated_data.get('password') else None
        if password and password != '':
            instance.set_password(password)
        instance.save()
        return instance
