from django.contrib import admin
from .models import FoodItems, orders, Feedback, OrderItems, Category

# Admin for Orders
class OrderAdmin(admin.ModelAdmin):
    list_display = ["student_username", "student_email", "order_date"]
    search_fields = ["student_username", "student_email"]

    def student_username(self, obj):
        return obj.student.username

    def student_email(self, obj):
        return obj.student.email


# Admin for OrderItems
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["food", "student_username", "quantity", "price"]
    search_fields = ["food__name", "orders__student__username"]

    def student_username(self, obj):
        return obj.orders.student.username


# Admin for Feedback
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["food_item", "student_username", "rating", "submission_date"]
    search_fields = ["food_item__name", "student__username"]

    def student_username(self, obj):
        return obj.student.username


# Register models
admin.site.register(FoodItems)
admin.site.register(orders, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(Category)
