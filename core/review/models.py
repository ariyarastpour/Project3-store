from django.db import models
from django.contrib.auth.models import User
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
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField('accounts.Profile', blank=True, related_name='liked_reviews')
    dislikes = models.ManyToManyField('accounts.Profile', blank=True, related_name='disliked_reviews')
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.product}" 

    @property
    def total_likes(self):
        return self.likes.count()
    
    @property
    def total_dislikes(self):
        return self.dislikes.count()
    
    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()
    
    def is_disliked_by(self, user):
        return self.dislikes.filter(id=user.id).exists()
    
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