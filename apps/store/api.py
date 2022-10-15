from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Store, Product, Variant 
from .serializers import ProductSerializer, VariantSerializer

# PERMISSIONS:

class TokenCheck():
    message = "Invalid token"
    
    def has_permission(self, request, view):
        requested_storeID = request.headers.get('storeID')
        requested_token = request.headers.get('token')

        store = Store.objects.get(id=requested_storeID)

        if store.token == requested_token:
            return True
        else:
            return False

# ENDPOINTS:

@api_view(['GET'])
@permission_classes([TokenCheck])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([TokenCheck])
def specific_product(request, product_id):
    products = Product.objects.get(id=product_id)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([TokenCheck])
def all_variants(request, product_id):
    variant = Variant.objects.filter(product__id=product_id)
    serializer = VariantSerializer(variant, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([TokenCheck])
def specific_variant(request, variant_id):
    variant = Variant.objects.get(id=variant_id)
    serializer = VariantSerializer(variant, many=False)
    return Response(serializer.data)