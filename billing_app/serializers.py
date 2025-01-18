import math
import random
from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PurchaseItemSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField()

    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'amount', 'purchase']

    # need to add unit price, purchase price, tax (%), tax amount

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product_id'] = instance.product.product_id
        response['one_unit_price'] = instance.product.one_unit_price
        response['tax_percentage'] = instance.product.tax_percentage
        response['tax_amount'] = instance.product.calculate_tax() * instance.quantity
        response['purchase_price'] = instance.product.one_unit_price * instance.quantity
        return response

    def create(self, validated_data):
        product = Product.objects.filter(id=validated_data['product']).first()
        return PurchaseItem.objects.create(
            product=product,
            quantity=validated_data['quantity'],
            purchase=validated_data['purchase']
        )

class PurchaseDetailsSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)

    class Meta:
        model = PurchaseDetails
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer_email'] = instance.customer.customer_email
        response['total_amount_without_tax'] = f"{(int(instance.total_amount) - int(instance.total_tax)):.1f}"
        round_value = math.floor(instance.total_amount)
        response['total_amount_round_value'] = f"{round_value:.1f}"
        response['payable_amount_to_customer'] = f"{(int(instance.customer_paid_amount) - int(instance.total_amount)):.1f}"
        return response
    

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase_count = PurchaseDetails.objects.all().count() + 1
        random_number = random.randint(100000, 999999)
        purchase_no = f'PUR-NO-{random_number}-{purchase_count}'
        validated_data['purchase_no'] = purchase_no
        purchase = PurchaseDetails.objects.create(**validated_data)
        total_amount = 0
        total_tax = 0
        for item_data in items_data:
            product_id = item_data['product']
            product = Product.objects.filter(id=product_id).first()
            item = PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=item_data['quantity']
            )
            total_amount += item.amount
            total_tax += product.calculate_tax() * item_data['quantity']
        
        purchase.total_amount = total_amount
        purchase.total_tax = total_tax
        purchase.save()
        return purchase


class DenominationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denomination
        fields = '__all__'
        