from rest_framework import viewsets
from .models import Category, Provider, Service
from .serializers import CategorySerializer, ProviderSerializer, ServiceSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.select_related('user').all()
    serializer_class = ProviderSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('provider__user', 'category').all()
    serializer_class = ServiceSerializer