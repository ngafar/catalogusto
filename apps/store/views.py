from django import forms 
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Store, Product, Variant 
from .forms import StoreForm, ProductForm, VariantForm
from . import stripe_utils

def dashboard(request):
    context_dict = {}
    
    stores = Store.objects.all()
    context_dict['stores'] = stores

    return render(request, 'store/dashboard.html', context_dict)


#----------------
# STORE
#----------------

def create_store(request):
    context_dict = {}

    if request.method == 'POST':
        store_form = StoreForm(data=request.POST)

        if store_form.is_valid():
            store = store_form.save()
            store.save()

            return HttpResponseRedirect(f'/store/{store.id}')
    else:
        store_form = StoreForm()

    context_dict['store_form'] = store_form

    return render(request, 'store/store-create.html', context_dict)

def read_store(request, store_id):
    context_dict = {}
    
    store = Store.objects.get(id=store_id)
    context_dict['store'] = store

    products = Product.objects.filter(store__id=store_id)
    context_dict['products'] = products

    return render(request, 'store/store-read.html', context_dict) 

def update_store(request, store_id):
    context_dict = {}

    store = Store.objects.get(id=store_id)
    context_dict['store'] = store

    if request.method == 'POST':
        store_form = StoreForm(data=request.POST, instance=store)

        if store_form.is_valid():
            store = store_form.save()
            store.save()

            return HttpResponseRedirect(f'/store/{store.id}')
    else:
        store_form = StoreForm(instance=store)

    context_dict['store_form'] = store_form

    return render(request, 'store/store-update.html', context_dict)

def delete_store(request, store_id):
    store = Store.objects.get(id=store_id) 
    store.delete()
    
    return HttpResponseRedirect(f'/dashboard')


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
            
            # Stripe
            stripe_prod_obj = stripe_utils.create_product(product.name, store.currency, product.price, store.stripe_secret_key) 

            product.stripe_prod_id = stripe_prod_obj['id']
            product.save()

            return HttpResponseRedirect(f'/product/{product.id}')
    else:
        product_form = ProductForm()
        product_form.fields['store'].widget = forms.HiddenInput()

    context_dict['product_form'] = product_form

    return render(request, 'store/product-create.html', context_dict)

def update_product(request, product_id):
    context_dict = {}

    product = Product.objects.get(id=product_id) 
    context_dict['product'] = product
    
    old_price_val = product.price

    variants = Variant.objects.filter(product__id=product_id)
    context_dict['variants'] = variants 

    if request.method == 'POST':
        product_form = ProductForm(data=request.POST, instance=product)
        product_form.fields['store'].widget = forms.HiddenInput()

        if product_form.is_valid():
            prod = product_form.save()
            prod.save()

            # Stripe
            price_change = True if prod.price != old_price_val else False
            stripe_utils.update_product(
                product.stripe_prod_id, 
                prod.name, 
                product.store.currency, 
                prod.price, 
                price_change, 
                product.store.stripe_secret_key)

            return HttpResponseRedirect(f'/product/{product.id}')
    else:
        product_form = ProductForm(instance=product)
        product_form.fields['store'].widget = forms.HiddenInput()

    context_dict['product_form'] = product_form

    return render(request, 'store/product-update.html', context_dict)

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id) 
    product.delete()
    
    return HttpResponseRedirect(f'/store/{product.store.id}/')


#----------------
# VARIANT
#----------------

def create_variant(request, product_id):
    context_dict = {}

    product = Product.objects.get(id=product_id)
    context_dict['product'] = product

    if request.method == 'POST':
        variant_form = VariantForm(data=request.POST)
        variant_form.fields['product'].widget = forms.HiddenInput()

        if variant_form.is_valid():
            variant = variant_form.save()
            variant.product = product

            # Stripe
            stripe_prod_obj = stripe_utils.create_product(
                f'{product.name} - {variant.name}', 
                product.store.currency, 
                variant.price, 
                product.store.stripe_secret_key)

            variant.stripe_prod_id = stripe_prod_obj['id']
            variant.save()

            # Add variant to M2M field in Product model:
            product.variants.add(variant)

            return HttpResponseRedirect(f'/product/{product.id}')
    else:
        variant_form = VariantForm()
        variant_form.fields['product'].widget = forms.HiddenInput()

    context_dict['variant_form'] = variant_form

    return render(request, 'store/variant-create.html', context_dict)

def update_variant(request, variant_id):
    context_dict = {}

    variant = Variant.objects.get(id=variant_id)
    context_dict['variant'] = variant

    old_price_val = variant.price

    if request.method == 'POST':
        variant_form = VariantForm(data=request.POST, instance=variant)
        variant_form.fields['product'].widget = forms.HiddenInput()

        if variant_form.is_valid():
            var = variant_form.save()
            var.save()

            # Stripe
            price_change = True if variant.price != old_price_val else False
            stripe_utils.update_product(
                variant.stripe_prod_id, 
                f'{variant.product.name} - {variant.name}', 
                variant.product.store.currency, 
                variant.price, 
                price_change, 
                variant.product.store.stripe_secret_key)

            return HttpResponseRedirect(f'/product/{variant.product.id}')
    else:
        variant_form = VariantForm(instance=variant)
        variant_form.fields['product'].widget = forms.HiddenInput()

    context_dict['variant_form'] = variant_form

    return render(request, 'store/variant-update.html', context_dict)

def delete_variant(request, variant_id):
    variant = Variant.objects.get(id=variant_id)
    variant.delete()
    
    return HttpResponseRedirect(f'/product/{variant.product.id}')