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
    product = ProductSerializer()

    class Meta:
        model = PurchaseItem
        fields = '__all__'

class PurchaseDetailsSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)

    class Meta:
        model = PurchaseDetails
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = PurchaseDetails.objects.create(**validated_data)
        total_amount = 0
        total_tax = 0
        for item_data in items_data:
            product = item_data['product']
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
