# views.py
import threading
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
    denomination_querysets = Denomination.objects.all().order_by('-label_value')
    context = {
        "denomination_querysets":denomination_querysets,
    }
    return render(request, 'pages/billing_page.html', context=context) 


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DenominationViewSet(viewsets.ModelViewSet):
    queryset = Denomination.objects.all().order_by('-label_value')
    serializer_class = DenominationSerializer


@api_view(['POST'])
def create_purchase(request):
    print(request.data)
    customer_email = request.data['email']
    customer_paid_amount = request.data['customer_paid_amount']
    customer = Customer.objects.filter(customer_email=customer_email).first()
    if not customer:
        customer_name = customer_email.split("@")[0]
        customer = Customer.objects.create(customer_email=customer_email, customer_name=customer_name)
    
    items_data = request.data.get('products', [])
    items = []
    for item in items_data:
        product = Product.objects.filter(id=item['product_id']).first()
        if product:
            items.append({
                'product': str(product.id),
                'quantity': item['quantity']
            })
    
    purchase_data = {
        'customer': customer.id,
        'items': items,
        "customer_paid_amount": customer_paid_amount
    }
    serializer = PurchaseDetailsSerializer(data=purchase_data)
    if serializer.is_valid():
        purchase = serializer.save()
        email_thread = threading.Thread(target=send_email_with_invoice, args=(customer.customer_email, purchase))
        email_thread.start() 
        data = serializer.data
        return Response({'msg': 'Bill Generated Successfully', 'data': data, 'purchase_id': purchase.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email_with_invoice(email, purchase):
    subject = f"Invoice for Purchase #{purchase.purchase_no}"
    message = f"Dear Customer,\n\nHere is your invoice for purchase - #{purchase.purchase_no}.\n\nTotal Amount: {purchase.total_amount}\nTotal Tax: {purchase.total_tax}\n\nThank you for shopping with us!"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email], fail_silently=False)


@api_view(['GET'])
def view_purchase(request, purchase_id):
    is_view = request.GET.get('view', False)
    try:
        purchase = PurchaseDetails.objects.get(id=purchase_id)
    except PurchaseDetails.DoesNotExist:
        return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PurchaseDetailsSerializer(purchase).data
    denom = denomination(float(serializer.get('payable_amount_to_customer')))

    if not is_view:
        serializer['billing_denominations'] = denom
        serializer['heading'] = "Generated Bill"
    else:
        serializer['heading'] = "Bill View"


    return render(request, 'pages/generate_bill.html', context=serializer) 



def denomination(balance):
    denomination_objects = Denomination.objects.filter(count__gt= 0).all()
    denominations = denomination_objects.values_list('label_value', flat=True)

    denomination_dict = { str(denomi.label_value) : str(denomi.count) for denomi in denomination_objects}

    balance = int(balance)
    result = {}

    for denom in denominations:
        count_value = balance // denom 
        if count_value > 0 and int(denomination_dict[str(denom)]) > int(count_value):
            result[denom] = count_value 
            balance %= denom
    return result


@api_view(['GET'])
def purchase_list(request):
    """
    Here we get the purchase details list
    """

    querysets = PurchaseDetails.objects.all().order_by('-purchase_date')

    context = {
        "querysets": querysets
    }

    return render(request, 'pages/purchase_list_page.html', context=context) 