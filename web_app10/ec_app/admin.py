from django.contrib import admin
from .models import Product, Order
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
