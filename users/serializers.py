from rest_framework import serializers, status
from .models import User
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password']


    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        if User.objects.filter(username=username):
            raise ValidationError({'error': f' {username} is  already exists'}  )
        elif User.objects.filter(email=email):
            raise ValidationError({'error': f'{email} is already exists'})
        elif User.objects.filter(phone_number=phone_number):
            raise ValidationError({'error': f'{phone_number} is already exists'})
        return attrs


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class ValidationErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()