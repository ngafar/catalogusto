import stripe
from django import forms 
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Store, Product, Variant 
from .forms import ProductForm, VariantForm

def dashboard(request):
    context_dict = {}
    
    stores = Store.objects.all()
    context_dict['stores'] = stores

    return render(request, 'store/dashboard.html', context_dict)

#----------------
# STORE
#----------------

def create_store(request):
    pass 

def read_store(request, store_id):
    context_dict = {}

    products = Product.objects.filter(store__id=store_id)
    context_dict['products'] = products

    return render(request, 'store/store-read.html', context_dict) 

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
                default_price_data = {
                    'currency': store.currency, 
                    'unit_amount_decimal': product.price * 100},
                api_key = store.stripe_secret_key)

            product.stripe_prod_id = stripe_prod_obj['id']
            product.save()

            return HttpResponseRedirect(f'/product/{product.id}/edit')
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
            #prod.store = store

            if product.price != old_price_val:
                # Retrieve product from Stripe:
                stripe_prod_obj = stripe.Product.retrieve(
                    product.stripe_prod_id, 
                    api_key = product.store.stripe_secret_key)
                
                old_price_stripe_id = stripe_prod_obj['default_price']

                # Add new price:
                new_price = stripe.Price.create(
                    product = stripe_prod_obj['id'],
                    currency = product.store.currency,
                    unit_amount_decimal = product.price * 100,
                    api_key = product.store.stripe_secret_key)

                # Update name + set new default price in Stripe:
                stripe.Product.modify(
                    product.stripe_prod_id,
                    name = product.name, 
                    default_price = new_price['id'],
                    api_key = product.store.stripe_secret_key)

                # Deactivate old price in Stripe:
                stripe.Price.modify( 
                    old_price_stripe_id,
                    active = "false",
                    api_key = product.store.stripe_secret_key)
            else:
                # Only update name in Stripe:
                stripe.Product.modify(
                    product.stripe_prod_id,
                    name = product.name, 
                    api_key = product.store.stripe_secret_key)

            #prod.stripe_prod_id = stripe_prod_obj['id']
            prod.save()

            return HttpResponseRedirect(f'/product/{product.id}/edit')
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

            # Create product in Stripe:
            stripe_prod_obj = stripe.Product.create(
                name = f'{product.name} - {variant.name}', 
                default_price_data = {
                    'currency': product.store.currency, 
                    'unit_amount_decimal': variant.price * 100},
                api_key = product.store.stripe_secret_key)

            variant.stripe_prod_id = stripe_prod_obj['id']
            variant.save()

            return HttpResponseRedirect(f'/product/{product.id}/edit')
    else:
        variant_form = VariantForm()
        variant_form.fields['product'].widget = forms.HiddenInput()

    context_dict['variant_form'] = variant_form

    return render(request, 'store/variant-create.html', context_dict)

def update_variant(request, variant_id):
    context_dict = {}

    variant = Variant.objects.get(id=variant_id)
    old_price_val = variant.price

    if request.method == 'POST':
        variant_form = VariantForm(data=request.POST, instance=variant)
        variant_form.fields['product'].widget = forms.HiddenInput()

        if variant_form.is_valid():
            var = variant_form.save()
            #var.product = product

            if variant.price != old_price_val:
                # Retrieve product from Stripe:
                stripe_prod_obj = stripe.Product.retrieve(
                    variant.stripe_prod_id, 
                    api_key = variant.product.store.stripe_secret_key)
                
                old_price_stripe_id = stripe_prod_obj['default_price']

                # Add new price:
                new_price = stripe.Price.create(
                    product = stripe_prod_obj['id'],
                    currency = variant.product.store.currency,
                    unit_amount_decimal = variant.price * 100,
                    api_key = variant.product.store.stripe_secret_key)

                # Update name + set new default price in Stripe:
                stripe.Product.modify(
                    variant.stripe_prod_id,
                    name = f'{variant.product.name} - {variant.name}', 
                    default_price = new_price['id'],
                    api_key = variant.product.store.stripe_secret_key)

                # Deactivate old price in Stripe:
                stripe.Price.modify( 
                    old_price_stripe_id,
                    active = "false",
                    api_key = variant.product.store.stripe_secret_key)
            else:
                # Only update name in Stripe:
                stripe.Product.modify(
                    variant.stripe_prod_id,
                    name = f'{variant.product.name} - {variant.name}', 
                    api_key = variant.product.store.stripe_secret_key)

            var.save()

            return HttpResponseRedirect(f'/product/{variant.product.id}/edit')
    else:
        variant_form = VariantForm(instance=variant)
        variant_form.fields['product'].widget = forms.HiddenInput()

    context_dict['variant_form'] = variant_form

    return render(request, 'store/variant-update.html', context_dict)

def delete_variant(request, variant_id):
    variant = Variant.objects.get(id=variant_id)
    variant.delete()
    
    return HttpResponseRedirect(f'/product/{variant.product.id}/edit')