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

def bill(request):
    return render(request,'bill.html')


    
def foodbycategory(request,meal_type):
    category = get_object_or_404(Category,name=meal_type)



# Get search and sorting parameters
    query = request.GET.get('q', '')  

    sort_by = request.GET.get('sort')  # Default sorting by name

    # Define valid sorting fields
    valid_sort_fields = {
        # 'name':'name',
        'price': 'price',
        'created_at': 'created_at',
        'f_stock': 'f_stock'
    }
    
    # Ensure the selected sort option is valid
    # sort_field = valid_sort_fields.get(sort_by, 'name')
    sort_field = valid_sort_fields.get(sort_by, 'f_stock')
    sort_field = valid_sort_fields.get(sort_by, 'price')
    sort_field = valid_sort_fields.get(sort_by, 'created_at')

    query = request.GET.get('q', '')  # Get search query from URL parameters
    if query:
        latest_foods = FoodItems.objects.filter(category=category, name__icontains=query).order_by(sort_field)
  # Filter by search term
    else:
        latest_foods = FoodItems.objects.filter(category=category).order_by(sort_field)
  # Show all items in category

    # latest_foods=FoodItems.objects.filter(category=category)
    return render(request, 'food_list.html', {'latest_foods': latest_foods,'query': query,'sort_by': sort_by})


