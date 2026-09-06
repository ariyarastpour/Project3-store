from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

@api_view(["GET","POST"])
def ProductApiList(request):
    products = Product.objects.filter(status=1)
    if request.method == "GET":
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer  = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view()
def CategoryApiList(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return  Response(serializer.data)
