from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "dayly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(status=True)

    def lastmod(self, obj):
        return obj.updated_date