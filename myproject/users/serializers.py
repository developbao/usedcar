from rest_framework_mongoengine import serializers
from django.contrib.auth.hashers import make_password
from .models import User, UsedCar, CheckingCar, Admin, Order


class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'passwd': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['passwd'] = make_password(validated_data['passwd'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'passwd' in validated_data:
            validated_data['passwd'] = make_password(validated_data['passwd'])
        return super().update(instance, validated_data)


class UsedCarSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UsedCar
        fields = '__all__'


class CheckingCarSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CheckingCar
        fields = '__all__'


class AdminSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'passwd': {'write_only': True}
        }

# 序列化器，用于管理员注册
class AdminCreationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'passwd': {'write_only': True}
        }

    def validate_admin_key(self, value):
        if value != "2025":  # 只有正确的管理员密钥才能注册
            raise serializers.ValidationError("Invalid admin key")
        return value

    def create(self, validated_data):
        validated_data['passwd'] = make_password(validated_data['passwd'])  # 密码加密存储
        admin = Admin.objects.create(**validated_data)
        return admin

# 序列化器，用于管理员登录
class AdminLoginSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'passwd': {'write_only': True}
        }


class OrderSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Order
        fields = '__all__'
