from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(ProductModel)
admin.site.register(ProductUnit)
admin.site.register(Customer)
admin.site.register(Investor)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderUnit)