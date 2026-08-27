from django import template
from ..models import *

register = template.Library()

@register.inclusion_tag("includes/similar_prod.html", takes_context=True)
def show_similar_products(context, product):
    request = context["request"]
    similar_products = (
        Product.objects.filter(
            status=1,
            category__in=Category.objects.all()
        )
        .exclude(id=product.id)
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