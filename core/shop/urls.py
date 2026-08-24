from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.ListViewModel.as_view(), name='products'),
    path('products/list', views.ListViewModel.as_view(), name='list'),
    path("products/list/grid/", views.GridView.as_view(), name="list_grid"),
    path("product/<int:pk>/detail/", views.DetailViewModel.as_view(), name="detail"),
    # path("category/<slug:slug>", views.CategoryView.as_view(), name="category"),
]