from django.db import models

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