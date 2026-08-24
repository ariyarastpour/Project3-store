from django.contrib import admin
from .models import Review

@admin.register(Review)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rate")