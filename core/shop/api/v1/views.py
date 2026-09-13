from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
<<<<<<< Updated upstream
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ...models import Product, Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly
=======
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

>>>>>>> Stashed changes

# products
class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status=1)
    serializer_class = ProductSerializer
<<<<<<< Updated upstream
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["title"]
    ordering_fields = ["created_date"]
    pagination_class = CustomPagination
=======
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ["created_date"]
>>>>>>> Stashed changes


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permissions_classes = [IsAuthenticatedOrReadOnly]
