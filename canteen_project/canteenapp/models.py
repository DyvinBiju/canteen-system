from django.db import models
from django.contrib.auth.models import User

class FoodItems(models.Model):
    food_items = models.CharField(max_length=30)
    image = models.ImageField(upload_to='canteen_images/',null=True,blank=True)
    description = models.TextField(blank=True)
    f_stock = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    student = models.ForeignKey(User,on_delete=models.CASCADE)

class orders(models.Model):
    no_of_items_ordered = models.IntegerField()
    total_price = models.IntegerField()
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItems,on_delete=models.CASCADE)