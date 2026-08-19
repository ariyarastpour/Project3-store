from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Profile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email','is_active','is_staff','is_superuser']
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = [
        ('Authentication', {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_active","is_staff","is_superuser"]}),
        ("Group Permissions", {"fields": ["groups","user_permissions"]}),
        ("Last login", {"fields": ["last_login"]}),
    ]
    add_fieldsets = [
        (None,
            {
                "fields": ["email", "password1", "password2","is_active","is_staff","is_superuser"],
            },
        ),
    ]

admin.site.register(Profile)
admin.site.register(User,CustomUserAdmin)