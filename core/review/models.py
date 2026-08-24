from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from accounts.models import Profile
from django.utils import timezone
from shop.models import Product

class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5,
        validators=[MinValueValidator(0),MaxValueValidator(5)]
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        ordering = ["-created_date"]    

@receiver(post_save, sender=Review)
def create_profile(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        rates = Review.objects.filter(product=product).aggregate(
            Avg("rate")
        )["rate__avg"]
        product.avg_rate = round(rates, 1)
        product.save()