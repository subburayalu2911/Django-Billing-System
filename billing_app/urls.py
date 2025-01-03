from django.urls import path , include
from rest_framework.routers import DefaultRouter
from billing_app.views import *

app_name = 'billing_app'

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('customers', CustomerViewSet, basename='customers')

urlpatterns = [
    path('', billing_page, name='billing_page'),
    path('api/', include(router.urls)),
    path('create_purchase/', create_purchase, name='create_purchase'),
    path('view_purchase/<int:purchase_id>/', view_purchase, name='view_purchase'),
]