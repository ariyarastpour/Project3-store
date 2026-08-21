from django import template
from ..models import Heroslider, HeroBottomIcon

register = template.Library()

@register.inclusion_tag('includes/hero_slider.html')
def hero_slider():
    herosliders = Heroslider.objects.filter(status=True).order_by('-created_date')
    
    all_icons = HeroBottomIcon.objects.filter(heroslider__status=True).order_by('order')
    
    return {
        'herosliders': herosliders,
        'all_icons': all_icons,
    }