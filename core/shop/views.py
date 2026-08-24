from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from django.db.models import Count, Q
from django.core.exceptions import FieldError


class ListViewModel(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "shop/products-list.html"
    paginate_by = 9

    
    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)
    
    def get_queryset(self):
        queryset = Product.objects.filter(status=True)
        
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if minprice_q := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=minprice_q)
        if maxprice_q := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=maxprice_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["total_prod"] = self.get_queryset().count()
        return context
    

class GridView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "shop/products-grid.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(status=True)
        
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if minprice_q := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=minprice_q)
        if maxprice_q := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=maxprice_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["total_prod"] = self.get_queryset().count()
        return context


class DetailViewModel(DetailView):
    model = Product
    queryset = Product.objects.filter(status=True)
    context_object_name = 'product'
    template_name = "shop/products-detail.html"
    pk_url_kwarg = 'pk'