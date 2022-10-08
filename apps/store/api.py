from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Store, Product, Variant 
from .serializers import ProductSerializer

@api_view(['GET'])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def specific_product(request, product_id):
    products = Product.objects.filter(id=product_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
