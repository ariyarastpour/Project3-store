from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','created_date','updated_date']
    search_fields = ['title']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','user','status','created_date','published_date']
    list_filter = ('user',)
    search_fields = ('title',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(WishList)