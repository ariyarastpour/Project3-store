from rest_framework import serializers
from ...models import Product, Category
<<<<<<< Updated upstream
from django.urls import reverse
=======
from rest_framework.reverse import reverse
from accounts.models import Profile
>>>>>>> Stashed changes

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField(source="offer")
    relative_url = serializers.ReadOnlyField(source="get_absolute_url")
<<<<<<< Updated upstream
    absolute_url = serializers.SerializerMethodField(
        method_name="obj_absolute_url"
    )
=======
    absolute_url = serializers.SerializerMethodField(method_name="obj_absolute_url")
>>>>>>> Stashed changes

    class Meta:
        model = Product
        fields = [
<<<<<<< Updated upstream
            "id",
            'user',
            "category",
            "title",
            "slug",
            "description",
            "stock",
            "status",
            "price",
            "discount_percent",
            "discounted_price",
            "sells",
            "avg_rate",
            "relative_url",
            "absolute_url",
            "created_date",
            "updated_date",
        ]
        read_only_fields = [
            "user",
            "sells",
            "avg_rate",
            "created_date",
            "updated_date",
        ]

    
    def obj_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse("shop:shop-api-v1:products-detail", kwargs={"pk": obj.pk})
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url")
            rep.pop("absolute_url")
        rep["category"] = CategorySerializer(instance.category).data
        return rep
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
=======
            "id", "user", "category", "title", "slug", "image", "description",
            "stock", "status", "price", "discount_percent", "discounted_price",
            "sells", "avg_rate", "relative_url", "absolute_url",
            "created_date", "updated_date",
        ]
        read_only_fields = ["user", "sells", "avg_rate", "created_date", "updated_date"]
>>>>>>> Stashed changes

    def obj_absolute_url(self, obj):
        request = self.context.get("request")
        return reverse(
            "shop:shop-api-v1:product-detail",
            kwargs={"pk": obj.pk},
            request=request,
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("description", None)
        rep['category'] = CategorySerializer(instance.category).data
        return rep

    def create(self, validated_data):
        validated_data['user'] = Profile.objects.get(user__id = self.context.get("request").user.id)
        return super().create(validated_data)