from django.shortcuts import render, get_object_or_404,redirect
from .models import FoodItems
from .models import Category
from django.http import JsonResponse
from django.conf import settings



# Create your views here.

def index(request):
    
    return render(request,'index.html', {})

def home(request):
    # query category
    categories = Category.objects.all()
    return render(request,'home.html',{'categories':categories})

def layout(request):
    return render(request,'layout.html')

def bill(request):
    return render(request,'bill.html')


    
# def food_list(request):
#     category_id = request.GET.get('category_id')
    # category=Category.objects.get(category)
    #  ,name=meal_type)
    
    # if category_id:

    #     if Category.objects.filter(id=category_id).exists():
    #         category = Category.objects.get(id=category_id)
            

    #         latest_foods = FoodItems.objects.filter(category=category)
            
        
        

# Get search and sorting parameters
    # query = request.GET.get('q', '')  

    # sort_by = request.GET.get('sort')  


    # Define valid sorting fields
    # valid_sort_fields = {
    #     'name':'name',
    #     'price': 'price',
    #     'created_at': 'created_at',
    #     'f_stock': 'f_stock'
    # }
    
    # Ensure the selected sort option is valid
    # sort_field = valid_sort_fields.get(sort_by, 'name')


    # sort_field = valid_sort_fields.get(sort_by, 'f_stock')
    # sort_field = valid_sort_fields.get(sort_by, 'price')
    # sort_field = valid_sort_fields.get(sort_by, 'created_at')

    # query = request.GET.get('q', '')  
    # Get search query from URL parameters
    # if query:
    #     latest_foods = FoodItems.objects.filter(category=category, name__icontains=query).order_by(sort_field)
#   Filter by search term
    # else:
        


    # filter(category=category)
        
        # .order_by(sort_field)
  # Show all items in category

    # latest_foods=FoodItems.objects.filter(category=category)
    # return render(request, 'food_list.html', {'latest_foods': latest_foods})
    # ,'query': query,'sort_by': sort_by,})


# def food_list(request):
#     category_id = request.GET.get('category_id')
#     if category_id:
#         latest_foods = FoodItems.objects.filter(category_id=category_id)
    
#     return render(request, 'food_list.html', {'latest_foods': latest_foods,'query': query,'sort_by': sort_by,})


def food_list(request):
    category_id = request.GET.get('category_id')  # Get category ID from request
    query = request.GET.get('q', '')  # Get search query
    sort_by = request.GET.get('sort', '')  # Get sorting option

    latest_foods = FoodItems.objects.all()  # Default: fetch all food items

    if category_id and category_id.isdigit():  # Ensure category_id is a valid number
        category_id = int(category_id)
        latest_foods = latest_foods.filter(category_id=category_id)  # Filter by category

    if query:
        latest_foods = latest_foods.filter(name__icontains=query)  # Apply search filter

    if sort_by:
        latest_foods = latest_foods.order_by(sort_by)  # Apply sorting

    return render(request, 'food_list.html', {
        'latest_foods': latest_foods,
        'query': query,
        'sort_by': sort_by,
        'category_id': category_id if isinstance(category_id, int) else None  # Pass category_id safely
    })
