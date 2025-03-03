from django.contrib import admin

# Register your models here.
from.models import FoodItems,orders,Feedback,OrderItems, Category

from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    list_display = ["student__first_name", "student__email", "order_date"]
    search_fields = ["student__first_name"]


admin.site.register(FoodItems)
admin.site.register(orders, OrderAdmin)
admin.site.register(Feedback)
admin.site.register(OrderItems)
admin.site.register(Category)