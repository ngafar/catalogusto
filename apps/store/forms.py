from django import forms 
from .models import Store, Product, Variant 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['variants', 'stripe_prod_id',]