# views.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.core.mail import send_mail
from billing_project import settings
from django.shortcuts import render


def billing_page(request):
    """
    Navigate to billing page
    """
    return render(request, 'layout/billing_page.html') 


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@api_view(['POST'])
def create_purchase(request):
    try:
        customer_email = request.data['customer_email']
        customer = Customer.objects.get(email=customer_email)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    
    items_data = request.data.get('items', [])
    items = []
    for item in items_data:
        try:
            product = Product.objects.get(product_id=item['product_id'])
        except Product.DoesNotExist:
            return Response({"error": f"Product with ID {item['product_id']} not found"}, status=status.HTTP_404_NOT_FOUND)
        items.append({
            'product': product,
            'quantity': item['quantity']
        })
    
    purchase_data = {
        'customer': customer.id,
        'items': items
    }
    serializer = PurchaseDetailsSerializer(data=purchase_data)
    if serializer.is_valid():
        purchase = serializer.save()
        send_email_with_invoice(customer.email, purchase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email_with_invoice(email, purchase):
    subject = f"Invoice for Purchase #{purchase.name}"
    message = f"Dear Customer,\n\nHere is your invoice for purchase #{purchase.name}.\n\nTotal Amount: {purchase.total_amount}\nTotal Tax: {purchase.total_tax}\n\nThank you for shopping with us!"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email], fail_silently=False)


@api_view(['GET'])
def view_purchase(request, purchase_id):
    try:
        purchase = PurchaseDetails.objects.get(id=purchase_id)
    except PurchaseDetails.DoesNotExist:
        return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PurchaseDetailsSerializer(purchase)
    return Response(serializer.data)
