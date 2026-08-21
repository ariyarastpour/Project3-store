from django import template
from ..models import *

register = template.Library()

@register.inclusion_tag('includes/hero_slider.html')
def render_hero_slider():
    herosliders = Heroslider.objects.filter(status=True).order_by('-created_date')
    
    all_icons = HeroBottomIcon.objects.filter(heroslider__status=True).order_by('order')
    
    return {
        'herosliders': herosliders,
        'all_icons': all_icons,
    }


@register.inclusion_tag('includes/store_feature.html')
def render_store_features():
    features = StoreFeature.objects.filter(status=True).order_by('order')
    
    return {
        'features': features,
    }

@register.inclusion_tag('includes/brand_logo.html')
def render_brand_logos():
    brands = BrandLogo.objects.filter(status=True).order_by('order')
    
    return {
        'brands': brands,
    }