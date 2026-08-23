from django.contrib import admin
from .models import *

#Base.html
class HeaderMenuItemAdmin(admin.ModelAdmin):
    list_display = ['title','is_active','created_date','published_date']
    search_fields = ('title',)
    ordering = ('title',)

class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ['title','is_active','created_date','published_date']
    search_fields = ('title',)
    ordering = ('title',)

class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title','is_active','created_date','published_date']
    search_fields = ('title',)
    list_filter = ('column',)
    ordering = ('title',)

#Index.html
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

#About.html
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','role','created_date','published_date']
    search_fields = ('name',)
    list_filter = ('role',)
    ordering = ('name',)


admin.site.register(HeaderMenuItem,HeaderMenuItemAdmin)
admin.site.register(FooterColumn,FooterColumnAdmin)
admin.site.register(FooterLink,FooterLinkAdmin)
admin.site.register(BrandLogo,BrandLogoAdmin)
admin.site.register(Heroslider,HerosliderAdmin)
admin.site.register(StoreFeature,StoreFeaturesAdmin)
admin.site.register(HeroBottomIcon)
admin.site.register(TeamMember,TeamMemberAdmin)