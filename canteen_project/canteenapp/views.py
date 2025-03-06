from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodItems,orders,OrderItems
from .models import Category
from datetime import datetime

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
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    current_date = datetime.now().strftime('%Y-%m-%d')  # Format date as "YYYY-MM-DD"
    
    context = {
        'cart': cart,
        'total_price': total_price,
        'current_date': current_date,
        'user': request.user,  # Pass the logged-in user's info
    }
    return render(request,'bill.html',context)


    
def foodbycategory(request,meal_type):
    category = get_object_or_404(Category,name=meal_type)


def foodbycategory(request,meal_type):
    category = get_object_or_404(Category,name=meal_type)



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


def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})
    food_item = get_object_or_404(FoodItems, id=food_id)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form

    if str(food_id) in cart:
        cart[str(food_id)]['quantity'] += quantity
    else:
        cart[str(food_id)] = {
            'name': food_item.name,
            'quantity': quantity,
            'price': str(food_item.price)
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    for food_id, item in cart.items():
        food_item = FoodItems.objects.get(id=food_id)  # Retrieve the food item from the database
        item['image'] = food_item.image.url  # Get the image URL from the FoodItems model
        item['total'] = round(float(item['price']) * item['quantity'], 2)  # Calculate total for the item

    total_price = sum(item['total'] for item in cart.values())
    return render(request, 'view_cart.html', {'cart': cart, 'total_price': total_price})


def remove_from_cart(request, food_id):
    cart = request.session.get('cart', {})

    if str(food_id) in cart:
        del cart[str(food_id)]

    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if cart:
        order = orders.objects.create(student=request.user)

        for food_id, item in cart.items():
            food_item = FoodItems.objects.get(id=food_id)
            OrderItems.objects.create(
                food=food_item,
                orders=order,
                quantity=item['quantity'],
                price=food_item.price * item['quantity']
            )
        request.session['cart'] = {}  # Clear the cart

    return redirect('order_summary', order_id=order.id)

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

def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})
    food_item = get_object_or_404(FoodItems, id=food_id)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form

    if str(food_id) in cart:
        cart[str(food_id)]['quantity'] += quantity
    else:
        cart[str(food_id)] = {
            'name': food_item.name,
            'quantity': quantity,
            'price': str(food_item.price)
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    for food_id, item in cart.items():
        food_item = FoodItems.objects.get(id=food_id)  # Retrieve the food item from the database
        item['image'] = food_item.image.url  # Get the image URL from the FoodItems model
        item['total'] = round(float(item['price']) * item['quantity'], 2)  # Calculate total for the item

    total_price = sum(item['total'] for item in cart.values())
    return render(request, 'view_cart.html', {'cart': cart, 'total_price': total_price})


def remove_from_cart(request, food_id):
    cart = request.session.get('cart', {})

    if str(food_id) in cart:
        del cart[str(food_id)]

    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if cart:
        order = orders.objects.create(student=request.user)

        for food_id, item in cart.items():
            food_item = FoodItems.objects.get(id=food_id)
            OrderItems.objects.create(
                food=food_item,
                orders=order,
                quantity=item['quantity'],
                price=food_item.price * item['quantity']
            )
        request.session['cart'] = {}  # Clear the cart

    return redirect('order_summary', order_id=order.id)
