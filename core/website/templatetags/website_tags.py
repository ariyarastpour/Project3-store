from django import template
from ..models import *

register = template.Library()

#Base.html
@register.inclusion_tag('includes/header_menu.html')
def render_header_menu():
    items = HeaderMenuItem.objects.filter(is_active=True).order_by('order')
    return {'menu_items': items}


@register.inclusion_tag('includes/footer_menu.html')
def render_footer_menu():
    columns = FooterColumn.objects.filter(is_active=True).order_by('order')
    
    footer_data = []
    for column in columns:
        links = FooterLink.objects.filter(column=column, is_active=True).order_by('order')
        footer_data.append({
            'column': column,
            'links': links,
        })
    
    return {'footer_data': footer_data}
 

@register.inclusion_tag('includes/footer_socialmedia.html')
def render_socialmedia():
    socialmedias = SocialMedia.objects.filter(show_in_footer=True)
    return {'socialmedias': socialmedias}


#Index.html
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

#About.html
@register.inclusion_tag('includes/team_slider.html')
def render_team():
    members = TeamMember.objects.filter(is_active=True).order_by('order')
    return {'members': members}