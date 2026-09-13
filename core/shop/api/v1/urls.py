from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'shop-api-v1'


router = routers.DefaultRouter()
router.register('products', views.ProductModelViewSet, basename='products')
router.register('categories', views.CategoryModelViewSet, basename='category')
urlpatterns = router.urls


