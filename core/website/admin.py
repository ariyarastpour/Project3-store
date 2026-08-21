from django.contrib import admin
from .models import Heroslider,HeroBottomIcon
# Register your models here.

class HerosliderAdmin(admin.ModelAdmin):
    list_display = ['status','title','created_date','published_date']
    search_fields = ('title',)
    ordering = ('title',)

admin.site.register(Heroslider,HerosliderAdmin)
admin.site.register(HeroBottomIcon)
