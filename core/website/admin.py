# your_app/admin.py

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import *
from django.utils.safestring import mark_safe


class SocialMediaAdminForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = '__all__'
        widgets = {
            'url': forms.URLInput(attrs={'style': 'width: 400px;'}),
            'icon_class': forms.TextInput(attrs={'style': 'width: 200px;', 'placeholder': 'bi-facebook'}),
            'custom_icon_html': forms.Textarea(attrs={'rows': 2, 'style': 'width: 400px;'}),
            'custom_name': forms.TextInput(attrs={'style': 'width: 200px;'}),
        }
    
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
    list_filter = ('is_active', 'icon_style')
    search_fields = ('name', 'custom_name', 'url')
    
    fieldsets = (
        ('اطلاعات شبکه اجتماعی', {
            'fields': ('name', 'custom_name', 'url')
        }),
        ('تنظیمات آیکون', {
            'fields': ('icon', 'icon_style', 'icon_class', 'custom_icon_html', 'show_icon_preview'),
            'description': '''
                <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    <strong>راهنمای آیکون‌ها:</strong><br>
                    • <strong>تصویر</strong>: می‌توانید تصویر آپلود کنید<br>
                    • <strong>Bootstrap Icons</strong>: bi-facebook, bi-instagram, bi-twitter<br>
                    • <strong>Font Awesome</strong>: fab fa-facebook, fab fa-instagram<br>
                    • <strong>سایر</strong>: کد HTML دلخواه خود را وارد کنید
                </div>
            '''
        }),
        ('تنظیمات نمایش', {
            'fields': ('order', 'open_in_new_tab', 'is_active', 'show_in_footer')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'show_icon_preview')
    

    def show_icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" />',
                obj.icon.url
            )
        icon_html = obj.get_icon_html()
        if icon_html:
            return mark_safe(icon_html)
        return mark_safe('<span style="color: #999;">—</span>')
    
    show_icon_preview.short_description = "پیش‌نمایش آیکون"
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    get_display_name.short_description = "نام"
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} شبکه اجتماعی فعال شدند.')
    make_active.short_description = "فعال کردن شبکه‌های اجتماعی انتخاب شده"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} شبکه اجتماعی غیرفعال شدند.')
    make_inactive.short_description = "غیرفعال کردن شبکه‌های اجتماعی انتخاب شده"


# ============================================================
# =================== ۲. ادمین SiteSettings ===================
# ============================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # نمایش در لیست
    list_display = ('site_name', 'show_logo', 'phone', 'email', 'primary_color_preview')
    search_fields = ('site_name', 'phone', 'email', 'address')
    
    # گروه‌بندی فیلدها
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('طراحی و ظاهر', {
            'fields': ('primary_color', 'background_color', 'input_color', 
                      'font_family', 'custom_font_file', 'custom_font_name', 'use_custom_font')
        }),
        ('کپی‌رایت و توسعه‌دهنده', {
            'fields': ('copyright_start_year', 'developer_name', 'developer_url')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone', 'email', 'address', 'address_map')
        }),
        ('محتویات صفحات', {
            'fields': ('contact_content', 'privacy_content', 'About_content')
        }),
    )
    

    def show_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain;" />', obj.logo.url)
        return "—"
    show_logo.short_description = "لوگو"
    
    def primary_color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></div>',
            obj.primary_color
        )
    primary_color_preview.short_description = "رنگ اصلی"
    
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True


# ============================================================
# =================== ۳. ادمین HeaderMenuItem ===================
# ============================================================

@admin.register(HeaderMenuItem)
class HeaderMenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order', 'url')
    list_filter = ('is_active',)
    search_fields = ('title', 'url')
    
    fieldsets = (
        ('اطلاعات لینک', {
            'fields': ('title', 'url', 'order', 'is_active')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date')
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# =================== ۴. ادمین Footer ===================
# ============================================================

class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('title', 'url', 'order', 'is_active')
    ordering = ('order',)


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    inlines = [FooterLinkInline]
    list_display = ('title', 'link_count', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)
    
    fieldsets = (
        ('اطلاعات ستون', {
            'fields': ('title', 'order', 'is_active')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date')
    
    def link_count(self, obj):
        return obj.links.filter(is_active=True).count()
    link_count.short_description = "تعداد لینک‌ها"
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order', 'url')
    list_filter = ('is_active', 'column')
    search_fields = ('title', 'url')
    
    fieldsets = (
        ('اطلاعات لینک', {
            'fields': ('column', 'title', 'url', 'order', 'is_active')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date')
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# =================== ۵. ادمین Heroslider ===================
# ============================================================

class HeroBottomIconInline(admin.TabularInline):
    model = HeroBottomIcon
    extra = 1
    fields = ('image', 'title', 'order')


@admin.register(Heroslider)
class HerosliderAdmin(admin.ModelAdmin):
    inlines = [HeroBottomIconInline]
    list_display = ('title', 'show_image', 'status', 'created_date')
    list_editable = ('status',)
    list_filter = ('status', 'created_date')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('اطلاعات اسلایدر', {
            'fields': ('title', 'image', 'description', 'status')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date', 'show_image')
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 150px; height: auto;" />', obj.image.url)
        return "—"
    show_image.short_description = "پیش‌نمایش"
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


@admin.register(HeroBottomIcon)
class HeroBottomIconAdmin(admin.ModelAdmin):
    list_display = ('show_icon', 'title', 'heroslider', 'order')
    list_editable = ('order',)
    list_filter = ('heroslider',)
    
    def show_icon(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px;" />', obj.image.url)
        return "—"
    show_icon.short_description = "آیکون"


# ============================================================
# =================== ۶. ادمین StoreFeature ===================
# ============================================================

@admin.register(StoreFeature)
class StoreFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_icon', 'status', 'order')
    list_editable = ('status', 'order')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('اطلاعات ویژگی', {
            'fields': ('icon', 'title', 'description', 'status', 'order')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date', 'show_icon')
    
    def show_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 40px; height: 40px;" />', obj.icon.url)
        return "—"
    show_icon.short_description = "آیکون"
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# =================== ۷. ادمین BrandLogo ===================
# ============================================================

@admin.register(BrandLogo)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_icon', 'status', 'order')
    list_editable = ('status', 'order')
    list_filter = ('status',)
    search_fields = ('name',)
    
    fieldsets = (
        ('اطلاعات برند', {
            'fields': ('name', 'icon', 'status', 'order')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date', 'show_icon')
    
    def show_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 40px; height: 40px;" />', obj.icon.url)
        return "—"
    show_icon.short_description = "آیکون"
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# =================== ۸. ادمین TeamMember ===================
# ============================================================

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_image', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'role')
    search_fields = ('name', 'role', 'bio')
    
    fieldsets = (
        ('اطلاعات عضو تیم', {
            'fields': ('name', 'role', 'bio', 'image', 'order', 'is_active')
        }),
        ('اطلاعات مدیریتی', {
            'fields': ('created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date', 'show_image')
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover;" />', obj.image.url)
        return "—"
    show_image.short_description = "تصویر"
    
    def save_model(self, request, obj, form, change):
        if not obj.published_date:
            obj.published_date = now()
        super().save_model(request, obj, form, change)


# ============================================================
# =================== ۹. ادمین ContactMessage ===================
# ============================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_date', 'short_message')
    list_filter = ('created_date',)
    search_fields = ('name', 'last_name', 'email', 'phone_number', 'description')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('name', 'last_name', 'email', 'phone_number')
        }),
        ('متن پیام', {
            'fields': ('description',)
        }),
    )
    
    readonly_fields = ('name', 'last_name', 'email', 'phone_number', 'description', 'created_date')
    
    def full_name(self, obj):
        return f"{obj.name} {obj.last_name}"
    full_name.short_description = "نام کامل"
    
    def short_message(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    short_message.short_description = "متن پیام"
    
    def has_add_permission(self, request):
        return False  # کاربران نمیتوانند از ادمین پیام اضافه کنند


# admin.site.site_header = "پنل مدیریت فروشگاه"
# admin.site.site_title = "فروشگاه من"
# admin.site.index_title = "داشبورد مدیریت"