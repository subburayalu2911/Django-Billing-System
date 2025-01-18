from django.urls import path , include
from rest_framework.routers import DefaultRouter
from billing_app.views import *

app_name = 'billing_app'

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('customers', CustomerViewSet, basename='customers')
router.register('denominations', DenominationViewSet, basename='denomination')

urlpatterns = [
    path('', billing_page, name='billing_page'),
    path('api/', include(router.urls)),
    path('bill/create_purchase/', create_purchase, name='create_purchase'),
    path('bill/view_purchase/<uuid:purchase_id>/', view_purchase, name='view_purchase'),
    path('bill/purchase_list/', purchase_list, name='purchase_list'),
]