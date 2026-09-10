# website/admin.py

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import *


# ============================================================
# ===== کلاس پایه برای تنظیمات Singleton =====================
# ============================================================

class BaseSingletonAdmin(admin.ModelAdmin):
    """فقط یک رکورد قابل ایجاد است و نمی‌توان حذف کرد"""
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================
# ===== ۱. ادمین SocialMedia =================================
# ============================================================

class SocialMediaAdminForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        custom_name = cleaned_data.get('custom_name')
        icon_style = cleaned_data.get('icon_style')
        custom_icon_html = cleaned_data.get('custom_icon_html')
        
        if name == 'custom' and not custom_name:
            raise ValidationError("⚠️ لطفاً نام دلخواه را وارد کنید!")
        
        if icon_style == 'custom' and not custom_icon_html:
            raise ValidationError("⚠️ لطفاً کد HTML آیکون را وارد کنید!")
        
        return cleaned_data


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    form = SocialMediaAdminForm
    list_display = ('get_display_name', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order', 'url')
    search_fields = ('name', 'custom_name', 'url')
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    get_display_name.short_description = "نام"


# ============================================================
# ===== ۲. ادمین SiteSetting =================================
# ============================================================

@admin.register(SiteSetting)
class SiteSettingAdmin(BaseSingletonAdmin):
    list_display = ('site_name', 'show_logo', 'primary_color_preview')
    search_fields = ('site_name',)
    
    def show_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.logo.url)
        return "—"
    show_logo.short_description = "لوگو"
    
    def primary_color_preview(self, obj):
        return format_html(
            '<div style="width:30px; height:30px; background:{}; border-radius:4px;"></div>',
            obj.primary_color
        )
    primary_color_preview.short_description = "رنگ اصلی"


# ============================================================
# ===== ۳. ادمین AboutSetting ================================
# ============================================================

@admin.register(AboutSetting)
class AboutSettingAdmin(BaseSingletonAdmin):
    list_display = ('about_title',)
    search_fields = ('about_title', 'about_content')


# ============================================================
# ===== ۴. ادمین ContactSetting ==============================
# ============================================================

@admin.register(ContactSetting)
class ContactSettingAdmin(BaseSingletonAdmin):
    list_display = ('phone', 'email', 'address_short')
    search_fields = ('phone', 'email', 'address', 'contact_title')
    
    def address_short(self, obj):
        if obj.address:
            return obj.address[:40] + '...' if len(obj.address) > 40 else obj.address
        return "—"
    address_short.short_description = "آدرس"


# ============================================================
# ===== ۵. ادمین PrivacySetting ==============================
# ============================================================

@admin.register(PrivacySetting)
class PrivacySettingAdmin(BaseSingletonAdmin):
    list_display = ('page_title', 'last_update')
    search_fields = ('page_title', 'introduction_text')
    
    fieldsets = (
        ('اطلاعات عمومی صفحه', {
            'fields': ('page_title', 'page_subtitle', 'introduction_text')
        }),
    )


# ============================================================
# ===== ۶. ادمین PrivacySection ==============================
# ============================================================

@admin.register(PrivacySection)
class PrivacySectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('section_type', 'title', 'icon', 'is_active', 'order')
        }),
        ('توضیحات', {
            'fields': ('description',),
        }),
    )


# ============================================================
# ===== ۷. ادمین HeaderMenuItem ==============================
# ============================================================

@admin.register(HeaderMenuItem)
class HeaderMenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order', 'url')
    search_fields = ('title', 'url')
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# ===== ۸. ادمین Footer ======================================
# ============================================================


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    inlines = [FooterLinkInline]


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('column', 'is_active')
    search_fields = ('title', 'url')

# ============================================================
# ===== ۹. ادمین Heroslider ==================================
# ============================================================

class HeroBottomIconInline(admin.StackedInline):
    model = HeroBottomIcon
    extra = 0
    max_num = 1
    can_delete = True
    fields = ('image', 'title', 'order')
    verbose_name = 'آیکون پایین اسلایدر'
    verbose_name_plural = 'آیکون پایین اسلایدر'


@admin.register(Heroslider)
class HerosliderAdmin(admin.ModelAdmin):
    inlines = [HeroBottomIconInline]
    list_display = ('title', 'status', 'created_date')
    list_editable = ('status',)
    list_filter = ('status',)
    search_fields = ('title', 'description')
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


@admin.register(HeroBottomIcon)
class HeroBottomIconAdmin(admin.ModelAdmin):
    list_display = ('title', 'heroslider', 'order')
    list_editable = ('order',)
    list_filter = ('heroslider',)


# ============================================================
# ===== ۱۰. ادمین StoreFeature ===============================
# ============================================================

@admin.register(StoreFeature)
class StoreFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order')
    list_editable = ('status', 'order')
    search_fields = ('title', 'description')
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# ===== ۱۱. ادمین BrandLogo ==================================
# ============================================================

@admin.register(BrandLogo)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'order')
    list_editable = ('status', 'order')
    search_fields = ('name',)
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# ===== ۱۲. ادمین TeamMember ================================
# ============================================================

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'role')
    search_fields = ('name', 'role', 'bio')
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# ===== ۱۳. ادمین ContactMessage =============================
# ============================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_date', 'short_message')
    list_filter = ('created_date',)
    search_fields = ('name', 'last_name', 'email', 'description')
    readonly_fields = ('name', 'last_name', 'email', 'phone_number', 'description', 'created_date')
    
    def full_name(self, obj):
        return f"{obj.name} {obj.last_name}"
    full_name.short_description = "نام کامل"
    
    def short_message(self, obj):
        return obj.description[:40] + '...' if len(obj.description) > 40 else obj.description
    short_message.short_description = "پیام"
    
    def has_add_permission(self, request):
        return False
    

# ============================================================
# ===== 14. ادمین Preloader =============================
# ============================================================

@admin.register(LoaderSetting)
class LoaderSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('وضعیت و زمان‌بندی', {
            'fields': ('is_active', 'minimum_display_time')
        }),
        ('محتوای متنی', {
            'fields': ('loading_text', 'loading_text_color')
        }),
        ('پس‌زمینه', {
            'fields': ('background_color',)
        }),
        ('لوگو', {
            'fields': ('logo', 'logo_width', 'logo_animation', 'logo_animation_duration'),
            'classes': ('collapse',)
        }),
        ('دایره‌ی چرخان (اسپینر)', {
            'fields': ('show_spinner', 'spinner_color', 'spinner_size'),
            'classes': ('collapse',)
        }),
        ('نوار پیشرفت', {
            'fields': ('show_progress_bar', 'progress_bar_color'),
            'classes': ('collapse',)
        }),
    )
    
    list_display = ('loading_text', 'is_active', 'background_color', 'logo_animation', 'updated_date')
    
    list_editable = ('is_active',)
    list_display_links = ('loading_text',)
    
    ordering = ('-updated_date',)
    
    def has_add_permission(self, request):
        if LoaderSetting.objects.exists():
            return False
        return True