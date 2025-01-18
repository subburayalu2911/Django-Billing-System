from django.db import models
import uuid
from django.core.validators import MinValueValidator
from billing_app.validators import validate_image_extension


class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    available_stock = models.IntegerField(blank=True, null=True)
    one_unit_price = models.FloatField(blank=True, null=True)
    tax_percentage = models.FloatField(blank=True, null=True)
    product_image = models.ImageField(blank=True, null=True, validators=[validate_image_extension],upload_to='product_image/')

    @property
    def product_image_url(self):
        image = self.product_image.url
        if image:
            image_url = image.replace('/media/media/', '/media/')
        else:
            image_url = None
        return image_url
    
    def __str__(self):
        return self.name
    
    def calculate_tax(self):
        return self.one_unit_price * (self.tax_percentage / 100)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(unique=True)
    customer_phone_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.customer_name


class PurchaseDetails(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    purchase_no = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(blank=True, null=True)
    total_tax = models.FloatField(blank=True, null=True)
    customer_paid_amount = models.FloatField(blank=True, null=True)

    
class PurchaseItem(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    purchase = models.ForeignKey(PurchaseDetails, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def save(self, *args, **kwargs):
        self.amount = self.product.one_unit_price * self.quantity + (self.product.calculate_tax() * self.quantity)
        super().save(*args, **kwargs)


class Denomination(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    label_value = models.DecimalField(max_digits=6, decimal_places=2, unique=True)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.label_value} - {self.count}"
