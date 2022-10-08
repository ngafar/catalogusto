from django.urls import path
from . import views, api

urlpatterns = [
    path('api/all-products/', api.all_products),
]