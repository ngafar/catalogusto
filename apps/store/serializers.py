from rest_framework import serializers
from .models import Store, Product, Variant 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant 
        fields = '__all__'        