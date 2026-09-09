from django.urls import path, include, re_path
from . import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.ListViewModel.as_view(), name='products'),
    path('products/list/', views.ListViewModel.as_view(), name='list'),
    path("products/grid/", views.GridView.as_view(), name="list_grid"),
    re_path(r'^product/(?P<slug>[-\w\u0600-\u06FF]+)/$', views.DetailViewModel.as_view(), name='detail'),
    path("category/<slug:slug>/", views.CategoryView, name="category"),
    path("api/v1/", include("shop.api.v1.urls")),
]