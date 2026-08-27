from django.db import models
from accounts.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    user = models.ForeignKey("accounts.Profile",on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,allow_unicode=True)
    image = models.ImageField(upload_to='img/products/')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    stock = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=0, max_digits=10)
    discount_percent = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    sells = models.PositiveIntegerField(default=0)
    avg_rate = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def offer(self):
        if self.discount_percent:
            return self.price - (self.price * self.discount_percent) / 100
        return self.price

    def is_published(self):
        return self.status == True

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_date']

    def get_absolute_url(self):
        return reverse("shop:detail", kwargs={"slug": self.slug})
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='img/product-gallery/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)

    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.title} - Image {self.order}"


class WishList(models.Model):
    user = models.ForeignKey("accounts.user", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} , {self.product}"