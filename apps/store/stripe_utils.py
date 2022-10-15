import stripe

def create_product(name, currency, price, api_key):
    stripe_prod_obj = stripe.Product.create(
        name = name, 
        default_price_data = {
            'currency': currency, 
            'unit_amount_decimal': price * 100},
        api_key = api_key)    

    return stripe_prod_obj

def update_product(stripe_prod_id, name, currency, price, price_change, api_key):
    if price_change:
        # Retrieve product from Stripe:
        stripe_prod_obj = stripe.Product.retrieve(
            stripe_prod_id, 
            api_key = api_key)
        
        old_price_stripe_id = stripe_prod_obj['default_price']

        # Add new price:
        new_price = stripe.Price.create(
            product = stripe_prod_obj['id'],
            currency = currency,
            unit_amount_decimal = price * 100,
            api_key = api_key)

        # Update name + set new price as default in Stripe:
        stripe.Product.modify(
            stripe_prod_id,
            name = name, 
            default_price = new_price['id'],
            api_key = api_key)

        # Deactivate old price in Stripe:
        stripe.Price.modify( 
            old_price_stripe_id,
            active = "false",
            api_key = api_key)
    else:
        # Only update name in Stripe:
        stripe.Product.modify(
            stripe_prod_id,
            name = name, 
            api_key = api_key)
