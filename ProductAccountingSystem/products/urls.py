from django.urls import path
from products.views import *

urlpatterns = [
    path('', all_products, name='main'),
]