from django.urls import path
from . import views, api

urlpatterns = [
    # views.py
    path('store/create/', views.create_store),
    path('store/read/<int:store_id>/', views.read_store),
    path('store/update/<int:store_id>/', views.update_store),
    path('store/delete/<int:store_id>/', views.delete_store),
    
    path('product/create/', views.create_product),
    path('product/read/<int:product_id>/', views.read_product),
    path('product/update/<int:product_id>/', views.update_product),
    path('product/delete/<int:product_id>/', views.delete_product),

    path('variant/create/', views.create_variant),
    path('variant/read/<int:variant_id>/', views.read_variant),
    path('variant/update/<int:variant_id>/', views.update_variant),
    path('variant/delete/<int:variant_id>/', views.delete_variant),

    # api.py
    path('api/all-products/', api.all_products),
    path('api/product/<int:product_id>/', api.specific_product),
    path('api/all-variants/<int:product_id>/', api.all_variants),
    path('api/variant/<int:variant_id>/', api.specific_variant),
]