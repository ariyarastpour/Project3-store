from django.db import models

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
    image = models.ImageField(upload_to='staticfiles/img/160x160')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.heroslider.title} - {self.title or 'آیکون'}"