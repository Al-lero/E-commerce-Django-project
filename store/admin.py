from django.contrib import admin

from .models import Product, Collection


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'collections', 'inventory_status']
    list_per_page = 10
    list_editable = ['price', 'description']
    search_fields = ['name']

    @admin.display(ordering='inventory')
    def inventory_status(self, product: Product):
        if product.inventory < 20:
            return 'Low'

        return 'Ok'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # list_display_links = ('id',)
    list_display = ['id', 'name', 'product_count']
    list_per_page = 10

    # search_fields = ['name']
    @admin.display(ordering=Collection)
    def product_count(self, collection: Collection):
        return collection.product_set.count()
