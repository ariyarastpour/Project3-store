from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ...models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# products
class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status=1)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permissions_classes = [IsAuthenticatedOrReadOnly]