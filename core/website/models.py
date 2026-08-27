from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


class SocialMedia(models.Model):
    
    SOCIAL_CHOICES = [
        ('instagram', 'اینستاگرام'),
        ('telegram', 'تلگرام'),
        ('whatsapp', 'واتساپ'),
        ('twitter', 'توییتر'),
        ('youtube', 'یوتیوب'),
        ('linkedin', 'لینکدین'),
        ('aparat', 'آپارات'),
        ('facebook', 'فیسبوک'),
        ('tiktok', 'تیکتاک'),
        ('snapp', 'اسنپ'),
        ('google_play', 'گوگل پلی'),
        ('app_store', 'اپ استور'),
        ('custom', 'سایر (دلخواه)'),
    ]
    
    ICON_STYLE_CHOICES = [
        ('bi', 'Bootstrap Icons'),
        ('fab', 'Font Awesome (Brands)'),
        ('fas', 'Font Awesome (Solid)'),
        ('fa', 'Font Awesome'),
        ('custom', 'سایر'),
    ]
    
    name = models.CharField(
        max_length=20,
        choices=SOCIAL_CHOICES,
        verbose_name="نوع شبکه اجتماعی"
    )
    custom_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="نام دلخواه",
        help_text="اگر نوع 'سایر' را انتخاب کردید، نام دلخواه وارد کنید"
    )
    url = models.URLField(
        verbose_name="آدرس لینک",
        help_text="لینک کامل صفحه شبکه اجتماعی"
    )
    
    icon = models.ImageField(
        upload_to='social_media/icons/',
        blank=True,
        null=True,
        verbose_name="آیکون",
        help_text="تصویر آیکون با فرمت PNG یا SVG (حداقل ۳۲x۳۲ پیکسل)",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'webp']
            )
        ]
    )
    
    icon_class = models.CharField(
        max_length=100,
        verbose_name="کلاس آیکون",
        help_text="مثال: bi-facebook, bi-twitter, bi-instagram, bi-github",
        default="bi-link"
    )
    
    icon_style = models.CharField(
        max_length=20,
        choices=ICON_STYLE_CHOICES,
        default='bi',
        verbose_name="سبک آیکون",
        help_text="نوع کتابخانه آیکون"
    )
    
    custom_icon_html = models.TextField(
        blank=True,
        null=True,
        verbose_name="کد HTML آیکون دلخواه",
        help_text="اگر سبک 'سایر' را انتخاب کردید، کد HTML آیکون را اینجا وارد کنید"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    show_in_footer = models.BooleanField(
        default=False,
        verbose_name="نمایش در فوتر"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
        help_text="عدد کوچکتر، نمایش بالاتر"
    )
    open_in_new_tab = models.BooleanField(
        default=True,
        verbose_name="در تب جدید باز شود"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )
    
    class Meta:
        ordering = ['order', 'name']
        unique_together = ['name', 'url']
    
    def __str__(self):
        return self.get_display_name()
    
    def get_display_name(self):
        if self.name == 'custom' and self.custom_name:
            return self.custom_name
        return self.get_name_display()
    
    def get_icon_html(self):
        if self.icon:
            return f'<img src="{self.icon.url}" style="width: 24px; height: 24px; object-fit: contain;" />'
        
        if self.icon_style == 'custom' and self.custom_icon_html:
            return self.custom_icon_html
        
        if self.icon_style == 'bi' and self.icon_class:
            return f'<i class="bi {self.icon_class}"></i>'
        
        if self.icon_style == 'fab' and self.icon_class:
            return f'<i class="fab {self.icon_class}"></i>'
        
        if self.icon_style == 'fas' and self.icon_class:
            return f'<i class="fas {self.icon_class}"></i>'
        
        if self.icon_style == 'fa' and self.icon_class:
            return f'<i class="fa {self.icon_class}"></i>'
        
        return '<i class="bi-link"></i>'
    
    def save(self, *args, **kwargs):
        if self.name != 'custom':
            self.custom_name = None
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.icon:
            self.icon.delete(save=False)
        super().delete(*args, **kwargs)


# Site_settings
class SiteSettings(models.Model):
    logo = models.FileField(
        upload_to='site/logo/',
        blank=True,
        null=True,
        verbose_name="لوگوی سایت",
        help_text="فرمت SVG یا PNG با پس‌زمینه‌ی شفاف پیشنهاد می‌شود"
    )
    favicon = models.FileField(
        upload_to='site/favicon/',
        blank=True,
        null=True,
        verbose_name="فاوآیکون"
    )

    site_name = models.CharField(
        max_length=100,
        default="Front",
        verbose_name="نام سایت"
    )

    primary_color = models.CharField(
        max_length=7,
        default="#377DFF",
        verbose_name="رنگ اصلی تم",
        help_text="#377DFF کد هگز مثل"
    )
    background_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        verbose_name="رنگ پس‌زمینه‌ی اصلی"
    )

    input_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        verbose_name="رنگ فیلد ها(input)"
    )

    font_family = models.CharField(
        max_length=100,
        default='sans-serif',
        verbose_name="نام خانواده فونت (Font Family)",
        help_text="نام دقیق فونت را بنویسید، مثلاً: 'Vazirmatn', sans-serif"
    )

    custom_font_file = models.FileField(upload_to='fonts/', blank=True, null=True ,help_text='فایل با فرمت .woff2')
    custom_font_name = models.CharField(max_length=100, blank=True, help_text="نامی که برای فونت انتخاب می‌کنید (مثلاً: MyCustomFont)")
    use_custom_font = models.BooleanField(default=False)

    copyright_start_year = models.PositiveIntegerField(
        default=2024,
        verbose_name="سال شروع کپی‌رایت",
        help_text="مثلاً 2019 — سال پایان به‌صورت خودکار سال جاری در نظر گرفته می‌شود"
    )

    developer_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام سازنده/توسعه‌دهنده",
        help_text="مثلاً Dmitry Volkov — اگر خالی باشد این خط کلاً نمایش داده نمی‌شود"
    )

    developer_url = models.URLField(
        blank=True,
        verbose_name="لینک سازنده/توسعه‌دهنده"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="شماره تماس"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="ایمیل"
    )

    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="آدرس"
    )

    address_map = models.URLField(
        blank=True,
        null=True,
        help_text="لینک نقشه گوگل یا نشان",
        verbose_name="لینک نقشه"
    )

    contact_content = models.TextField(
        verbose_name="متن صفحه ارتباط با ما",
        default= 'ما همیشه خوشحال می‌شویم که به شما کمک کنیم و اطلاعات بیشتری درباره خدماتمان ارائه دهیم. می‌توانید از طریق ایمیل یا پر کردن فرم تماس با ما در ارتباط باشید. از اینکه ما را انتخاب کردید متشکریم!'
    )

    privacy_content = models.TextField(
        verbose_name="متن صفحه حریم خصوصی",
        default= 'ما همیشه خوشحال می‌شویم که به شما کمک کنیم و اطلاعات بیشتری درباره خدماتمان ارائه دهیم. می‌توانید از طریق ایمیل یا پر کردن فرم تماس با ما در ارتباط باشید. از اینکه ما را انتخاب کردید متشکریم!'
    )

    About_content = models.TextField(
        verbose_name="متن صفحه حریم خصوصی",
        default='شرکت ما با سال‌ها تجربه در زمینه فروش آنلاین، همواره تلاش کرده است بهترین خدمات را به مشتریان خود ارائه دهد.ما با ارائه محصولات باکیفیت و خدمات پس از فروش عالی، اعتماد شما را ارج می‌نهیم'
    )

    def __str__(self):
        return "تنظیمات عمومی سایت"
    
    def get_social_media(self):
        """دریافت لیست شبکه‌های اجتماعی فعال"""
        from .models import SocialMedia
        return SocialMedia.objects.filter(is_active=True).order_by('order')
    
    def get_social_media_json(self):
        """دریافت شبکه‌های اجتماعی به صورت JSON"""
        social_media = self.get_social_media()
        return [
            {
                'name': item.get_display_name(),
                'url': item.url,
                'open_in_new_tab': item.open_in_new_tab,
            }
            for item in social_media
        ]

    def save(self, *args, **kwargs):
        """قبل از ذخیره، بررسی کن که رکورد دیگری وجود نداشته باشد"""
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("⚠️ تنها یک رکورد برای تنظیمات سایت مجاز است!")
        super().save(*args, **kwargs)
    

# Base.html
class HeaderMenuItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان لینک")
    url = models.CharField(max_length=255, verbose_name="آدرس لینک")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class FooterColumn(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان ستون")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    column = models.ForeignKey(FooterColumn, on_delete=models.CASCADE, related_name='links', verbose_name="ستون والد")
    title = models.CharField(max_length=200, verbose_name="عنوان لینک")
    url = models.CharField(max_length=255, verbose_name="آدرس لینک")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.column.title} - {self.title}"
    

# Index.html
class Heroslider(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='staticfiles/img/mockups',default='staticfiles/img/600x600/img1.jpg')
    description = models.TextField()
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title


class HeroBottomIcon(models.Model):
    heroslider = models.ForeignKey(Heroslider, on_delete=models.CASCADE, related_name='bottom_icons')
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='img/160x160')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.heroslider.title} - {self.title or 'آیکون'}"
    

class StoreFeature(models.Model):
    icon = models.FileField(upload_to='svg/illustrations/', default='svg/illustrations/oc-protected-card.svg')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    

class BrandLogo(models.Model):
    name = models.CharField(max_length=200)
    icon = models.FileField(upload_to='svg/illustrations/')
    status = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    

#About.html
class TeamMember(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی")
    role = models.CharField(max_length=200, verbose_name="سمت (مثلاً: مدیر پروژه)")
    bio = models.TextField(blank=True, null=True, verbose_name="بیوگرافی کوتاه")
    image = models.ImageField(upload_to='team/', verbose_name="تصویر پروفایل")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['order']


    def __str__(self):
        return self.name
    

#Contact.html
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"