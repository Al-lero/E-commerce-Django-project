from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from decimal import Decimal

from store.models import Collection, Product, Cart, Review, CartItem, OrderItem, Order
from user.models import Customer


class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'cart', 'product', 'quantity']


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','total_price']

    def get_total_price(self, cart_items: CartItem):
        return cart_items.product.price * cart_items.quantity


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    class Meta:
        model = Cart
        fields = ['id', 'items','total_price']

    def get_total_price(self, cart: Cart):
       return sum ([item.quantity * item.price for item in cart.items.all()] )


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']
    # name =serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # inventory = serializers.IntegerField()
    # collection = serializers.CharField(max_length=255)
    collections = CollectionSerializer()
    # collections = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-details'
    # )
    discount = serializers.SerializerMethodField(method_name='discount_price')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'inventory', 'discount', 'collections']

    # collections = serializers.StringRelatedField()
    # discount = serializers.SerializerMethodField(method_name='discount_price')

    def discount_price(self, product: Product):
        return product.price * Decimal(0.10)


class CreateProductSerialization(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'inventory', 'collections']


class CreateCollectionSerialization(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'name', 'customer', 'content']


class CartProductSerializer (serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'description', 'price']

class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItem(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'place_at', 'payment_status', 'customer', 'order_item']
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            customer = get_object_or_404(Customer, id=user_id)
            order = Order.objects.create(customer=customer)
            cart_item = CartItem.objects.filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price
                ) for item in cart_item
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()
# class CartViewSet(CreateApiView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#
#
# class GetCartApiView()
