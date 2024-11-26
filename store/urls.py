from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

route = DefaultRouter()
route.register("collections", views.CollectionViewSet, basename='collections_list')
route.register("products", views.ProductViewSet, basename='products')
product_router = NestedDefaultRouter(route,  'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='products-review')
route.register("carts", views.CartViewSet, basename="carts")

route.register('orders', views.OrderViewSet, basename='order')

cart_item = NestedDefaultRouter(route, 'carts', lookup='cart')
cart_item.register('cart_items', views.CartItemViewSet, basename='cart_items')

print(product_router.urls)




#products/1/reviews (trying to build an endpoint for the review of a product)
#products/1/reviews/1

print(route.urls)

urlpatterns = route.urls + product_router.urls

# urlpatterns = [
#     path('',include(router.urls)),
#     path('products', views.ProductListView.as_view()),
#
#     path('products/<pk>/', views.ProductDetailsApiView.as_view()),
#
#     # path('cart', views.CreateCart.as_views()),
#
#     path('collections', views.collection_list),
#     # path('collections/<pk>', views.collection_details),
#     path('collections/<int:pk>/', views.collection_details, name='collection-details'),
#     # path('collections/<int:pk>/', views.CollectionDetailAPIViews.as_view(), name='collection-details'),
#     path('collections/<int:pk>/', views.CollectionListAPIViews.as_view(), name='collection-details')
# ]