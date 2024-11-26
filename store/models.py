from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings


# Create your models here.


class Collection(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product (models.Model):
    name = models.CharField(max_length=255,null=False, blank=False)
    description = models.CharField(max_length=255, null=False,blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveSmallIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotion = models.ManyToManyField('Promotion', related_name='+')

    def __str__(self):
        return f"{self.name} {self.price}"

    class Meta:
        ordering = ['name']


class Promotion(models.Model):
    product = models.ManyToManyField(Product, related_name='+')
    discount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product.name}"


class Cart(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4)
    create_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order (models.Model):
    PAYMENT_STATUS = [
        ('p', 'Pending'),
        ('S', 'Success'),
        ('F', 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default='')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class OrderItem (models.Model):
    quantity = models.PositiveIntegerField()
    unit_per_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Address (models.Model):
    number = models.PositiveIntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    content = models.TextField()





