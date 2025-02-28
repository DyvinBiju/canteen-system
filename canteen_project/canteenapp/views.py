from django.shortcuts import render, get_object_or_404
from .models import FoodItems
from .models import Category

# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def layout(request):
    return render(request,'layout.html')

def food_list(request):
    # Fetch the latest 6 food items from the database
    latest_foods = FoodItems.objects.order_by('-created_at')[:50]
    return render(request, 'food_list.html', {'latest_foods': latest_foods})


def food_detail(request, food_name):
    food = get_object_or_404(food_list, name=food_name)
    return render(request, 'canteenapp/food_detail.html', {'food': food})


