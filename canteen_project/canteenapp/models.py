from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
     created_at = models.DateTimeField(auto_now=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
          abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=30,unique=True)
    image = models.ImageField(upload_to='category_images/',null=True,blank=True)
    def __str__(self):
        return self.name



class FoodItems(TimeStampedModel):
    
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='canteen_images/',null=True,blank=True)
    description = models.TextField(blank=True)
    f_stock = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True,blank=False)

    def __str__(self):
        return self.name
    

class orders(TimeStampedModel):
    
    # total_price = models.IntegerField()
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    # food = models.ForeignKey(FoodItems,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student.first_name

class Feedback(TimeStampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItems, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comments = models.TextField(blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments

class OrderItems(TimeStampedModel):
     food = models.ForeignKey(FoodItems,on_delete=models.CASCADE)
     orders = models.ForeignKey(orders,on_delete=models.CASCADE)
     quantity = models.IntegerField()
     price = models.DecimalField(max_digits=10,decimal_places=2)

     def __str__(self):
        return self.food.name
