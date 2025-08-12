from contextvars import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from .models import Flower

User = get_user_model()

class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data.get("username"),
            password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Login yoki parol xato!")
        token, _ = Token.objects.get_or_create(user=user)
        return {
            "username": user.username,
            "token": token.key
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        read_only_fields = ['username', 'email']

