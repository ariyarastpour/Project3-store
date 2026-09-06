from django import template
from ..models import *
from django.db.models import Min

register = template.Library()

@register.inclusion_tag("includes/similar_prod.html", takes_context=True)
def show_similar_products(context, product):
    request = context["request"]
    similar_products = (
        Product.objects.filter(
            status=1,
            category=product.category
        )
        .distinct().exclude(id=product.id)
    )

    is_wished = []
    if request.user.is_authenticated:
        is_wished = WishList.objects.filter(user=request.user).values_list(
            "product_id", flat=True
        )

    context.update(
        {
            "similar_products": similar_products,
            "request": request,
            "is_wished": is_wished,
        }
    )
    return context


@register.inclusion_tag("includes/popular_product.html", takes_context=True)
def popular_products(context):
    request = context["request"]
    categories = Category.objects.all()
    
    categories_data = []
    
    for category in categories:
        products = Product.objects.filter(
            status=1,
            category=category
        ).order_by("-sells")[:3]
        
        min_price = Product.objects.filter(
            status=1,
            category=category
        ).aggregate(Min("price"))['price__min']
        
        categories_data.append({
            'category': category,
            'products': products,
            'min_price': min_price,
        })
    
    return {
        'categories_data': categories_data,
        'request': request,
    }


@register.inclusion_tag("includes/latest_prod.html", takes_context=True)
def show_latest_products(context):
    request = context["request"]
    latest_products = Product.objects.filter(
        status=1
    )[:8]

    is_wished = []
    if request.user.is_authenticated:
        is_wished = WishList.objects.filter(user=request.user).values_list(
            "product_id", flat=True
        )
    
    context.update(
        {
            "request": request,
            "latest_products": latest_products,
            "is_whished": is_wished
        }
    )
    return context