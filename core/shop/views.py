from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from django.db.models import Count, Q
from django.core.exceptions import FieldError
from review.models import Review


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        one_star = Count("rate",filter=Q(rate=1))
        two_star = Count("rate",filter=Q(rate=2))
        three_star = Count("rate",filter=Q(rate=3))
        four_star = Count("rate",filter=Q(rate=4))
        five_star = Count("rate",filter=Q(rate=5))
        product = self.get_object()
        reviews = Review.objects.filter(product=product)
        context["reviews"] = reviews
        context["reviews_status"] = reviews.aggregate(
            one_star=one_star,
            two_star=two_star,
            three_star=three_star,
            four_star=four_star,
            five_star=five_star
        )

        total_reviews = reviews.count()
        recommended = reviews.filter(rate__gte=4).count()
        
        if total_reviews > 0:
            context['recommend_percent'] = round((recommended / total_reviews) * 100)
        else:
            context['recommend_percent'] = 0

        return context
    

def CategoryView(request, slug):
    category = get_object_or_404(Category, slug=slug)    
    products = Product.objects.filter(status=1, category=category)
    
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'shop/products-list.html', context)