from django.contrib import admin

# Register your models here.
from.models import FoodItems,orders
admin.site.register(FoodItems)
admin.site.register(orders)