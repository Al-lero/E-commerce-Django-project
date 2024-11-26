import collections

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_nested.routers import NestedDefaultRouter


from store.filter import ProductFilter
from store.models import Product, Collection, Review, Cart, Order, CartItem
from .permissions import IsAdminOrReadOnly
from .serilizers import (ProductSerializer, CollectionSerializer, CreateProductSerialization, ReviewSerializer,
                         CartSerializer, CreateCollectionSerialization, CreateCartSerializer, CreateOrderSerializer,
                         OrderSerializer, AddToCartSerializer, UpdateCartItem, CartItemSerializer)


# Views is also the service.nm

#localhost:8000/store/products/
#localhost:8000/store/products/1


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CreateProductSerialization(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductListView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerialization


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterSet_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST':
            return CreateProductSerialization
        return ProductSerializer


class ProductCreate(CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerialization


class CollectionListAPIViews(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CreateCollectionSerialization

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CollectionSerializer
        elif self.request.method == 'POST':
            return CreateCollectionSerialization


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


# class CollectionDetailAPIViews(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CreateCollectionSerilization


class ProductDetailsApiView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerialization

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == "POST":
            return CreateProductSerialization


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        # product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = CollectionSerializer(Product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        product.delete()
        return Response(data={"message": f"Product with {pk} deleted"})


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItem
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}


@api_view()
def collection_list(request):
    collection = Collection.objects.all()
    serializer = CollectionSerializer(collection, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def collection_details(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(CreateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet,
                  RetrieveModelMixin):
    # created_at = models.DataTimeField(auto_now=True)
    queryset = Cart.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CreateCartSerializer
        return CreateCartSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
