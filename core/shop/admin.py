from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date', 'updated_date']
    search_fields = ['title']

    
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    fields = ['image', 'alt_text', 'order']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_date', 'published_date']
    list_filter = ('user',)
    search_fields = ('title',)
    inlines = [ProductGalleryInline]

class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'image']
    list_editable = ['order']
    search_fields = ['product__title']
    list_filter = ('product',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(WishList)