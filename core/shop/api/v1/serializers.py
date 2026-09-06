from rest_framework import serializers
from ...models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'user', 'title', 'category', 'status', 'stock', 'price', 'sells', 'created_date', 'published_date']

