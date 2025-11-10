from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Provider, Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )

    class Meta:
        model = Provider
        fields = ['id', 'user', 'user_id', 'phone', 'rating']


class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    provider = ProviderSerializer(read_only=True)

    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(),
        write_only=True,
        source='provider'
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'description', 'price',
            'category', 'provider',
            'category_id', 'provider_id',
            'created_at'
        ]
        read_only_files = ['created_at']
