from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','status','category','created_date','published_date']
    search_fields = ['title']
    list_filter = ['category', 'author']

admin.site.register(Category)
admin.site.register(Post,PostAdmin)
