from django.urls import path
from . import views, api

urlpatterns = [
    # views.py
    path ('dashboard/', views.dashboard),

    path('store/new/', views.create_store),
    path('store/<int:store_id>/', views.read_store),
    path('store/<int:store_id>/settings/', views.update_store),
    path('store/<int:store_id>/delete/', views.delete_store),
    path('store/<int:store_id>/get-new-token/', views.new_store_token),
    
    path('store/<int:store_id>/add-product/', views.create_product),
    path('product/<int:product_id>/', views.update_product),
    path('product/<int:product_id>/delete/', views.delete_product),

    path('product/<int:product_id>/add-variant', views.create_variant),
    path('variant/<int:variant_id>/', views.update_variant),
    path('variant/<int:variant_id>/delete/', views.delete_variant),

    # api.py
    path('api/all-products/', api.all_products),
    path('api/product/<int:product_id>/', api.specific_product),
    path('api/all-variants/<int:product_id>/', api.all_variants),
    path('api/variant/<int:variant_id>/', api.specific_variant),
]