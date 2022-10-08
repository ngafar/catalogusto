from django.urls import path
from . import views, api

urlpatterns = [
    path('api/all-products/', api.all_products),
    path('api/product/<int:product_id>/', api.specific_product),
    path('api/variant/<int:variant_id>/', api.specific_variant),
]