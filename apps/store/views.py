import stripe
from django import forms 
from django.shortcuts import render
from .models import Store, Product, Variant 
from .forms import ProductForm

#----------------
# STORE
#----------------

def create_store(request):
    pass 

def read_store(request, store_id):
    pass 

def update_store(request, store_id):
    pass

def delete_store(request, store_id):
    pass 


#----------------
# PRODUCT
#----------------

def create_product(request, store_id):
    context_dict = {}

    store = Store.objects.get(id=store_id)
    context_dict['store'] = store

    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        product_form.fields['store'].widget = forms.HiddenInput()

        if product_form.is_valid():
            product = product_form.save()
            product.store = store

            # Create product in Stripe:
            stripe_prod_obj = stripe.Product.create(
                name = product.name, 
                api_key = store.stripe_secret_key)

            product.stripe_prod_id = stripe_prod_obj['id']
            product.save()

            return HttpResponseRedirect('/client/'+str(client.id))
    else:
        product_form = ProductForm()
        product_form.fields['store'].widget = forms.HiddenInput()

    context_dict['product_form'] = product_form

    return render(request, 'store/product-create.html', context_dict)

def read_product(request, product_id):
    context_dict = {}

    product = Product.objects.get(id=product_id) 
    context_dict['product'] = product

    return render(request, 'store/product-read.html', context_dict)

def update_product(request, product_id):
    pass

def delete_product(request, product_id):
    pass 


#----------------
# VARIANT
#----------------

def create_variant(request):
    pass

def read_variant(request, variant_id):
    pass 

def update_variant(request, variant_id):
    pass

def delete_variant(request, variant_id):
    pass 