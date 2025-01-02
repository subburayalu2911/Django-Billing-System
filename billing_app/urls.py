from django.urls import path 
from billing_app.views import *

app_name = 'billing_app'

urlpatterns = [
    path('', billing_page, name='billing_page'),
    path('products/', product_list, name='product_list'),
    path('customers/', customer_list, name='customer_list'),
    path('create_purchase/', create_purchase, name='create_purchase'),
    path('view_purchase/<int:purchase_id>/', view_purchase, name='view_purchase'),
]