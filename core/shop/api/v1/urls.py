from django.urls import path
from . import views

app_name = 'shop-api-v1'

urlpatterns = [
    path('products/', views.ProductApiList, name="products-list"),
    path('categories/', views.CategoryApiList, name="categories-list"),
]
