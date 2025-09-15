from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import CustomUser

user = get_user_model()

# ----------------------------
# Register
# ----------------------------


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'address',
            'password',
            'is_seller'
        ]

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
            is_seller=validated_data.get('is_seller', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# ----------------------------
# User Profile
# ----------------------------


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id', 'username']

# ----------------------------
# Reset Password
# ----------------------------

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

