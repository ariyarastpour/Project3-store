from django.contrib import admin
from .models import *
# Register your models here.

class HerosliderAdmin(admin.ModelAdmin):
    list_display = ['title','status','created_date','published_date']
    search_fields = ('title',)
    ordering = ('title',)

class StoreFeaturesAdmin(admin.ModelAdmin):
    list_display = ['title','status','created_date','published_date']
    search_fields = ('title',)
    ordering = ('title',)

class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ['name','status','created_date','published_date']
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(BrandLogo,BrandLogoAdmin)
admin.site.register(Heroslider,HerosliderAdmin)
admin.site.register(StoreFeature,StoreFeaturesAdmin)
admin.site.register(HeroBottomIcon)