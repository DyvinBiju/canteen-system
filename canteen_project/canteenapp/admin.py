from django.contrib import admin

# Register your models here.
from.models import FoodItems,orders,Feedback,OrderItems
admin.site.register(FoodItems)
admin.site.register(orders)
admin.site.register(Feedback)
admin.site.register(OrderItems)
