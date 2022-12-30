from django.urls import path
from products.views import *
from users.views import authorization

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('', general_table, name='general_table'),
    path('all_products', all_products, name='all_products'),
    path('<int:id>', product_card, name='product_card'),

]