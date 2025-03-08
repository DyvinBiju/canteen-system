from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
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

def about(request):
    return render(request,'about.html',)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, "Profile updated successfully!")
        return render(request, 'profile.html')  # Render instead of redirect

    return render(request, 'profile.html')


    

def layout(request):
    return render(request,'layout.html')

def bill(request):
    cart = request.session.get('cart', {})
    current_date = datetime.now().strftime('%Y-%m-%d')  # Format date as "YYYY-MM-DD"
    total_price = 0
    for food_id, item in cart.items():
        item_price = float(item['price'])  # Ensure price is a float
        item_quantity = int(item['quantity'])  # Ensure quantity is an integer
        item_total = item_price * item_quantity  # Correct total calculation
        item['total'] = round(item_total, 2)  # Round to 2 decimal places
        total_price += item_total  # Add to grand total
    context = {
        'cart': cart,
        'total_price': total_price,
        'current_date': current_date,
        'user': request.user,  # Pass the logged-in user's info
    }
    return render(request,'bill.html',context)


@login_required(login_url='login') 
def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})
    food_item = get_object_or_404(FoodItems, id=food_id)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form
    
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add items to the cart.")
        return redirect('login')
    elif str(food_id) in cart:
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
    updated_cart = {}

    for food_id, item in cart.items():
        try:
            food_item = FoodItems.objects.get(id=food_id)  # Retrieve the food item from the database
            updated_cart[food_id] = {
                'name': food_item.name,
                'price': float(food_item.price),
                'quantity': item['quantity'],
                'image': food_item.image.url if food_item.image else None,  # Get the image URL
                'total': round(float(food_item.price) * item['quantity'], 2)  # Calculate total for the item
            }
        except FoodItems.DoesNotExist:
            continue  # Skip if food item is not found

    total_price = sum(item['total'] for item in updated_cart.values())

    return render(request, 'view_cart.html', {'cart': updated_cart, 'total_price': total_price})

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


def food_list(request):
    category_id = request.GET.get('category_id')  # Get category ID from request
    query = request.GET.get('q', '')  # Get search query
    sort_by = request.GET.get('sort', '')  # Get sorting option

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
    
    latest_foods = FoodItems.objects.all()  # Default: fetch all food items

    if category_id:  # Ensure category_id is a valid number
        # category_id = int(category_id)
        latest_foods = latest_foods.filter(category_id=category_id)  # Filter by category
        print(latest_foods)
    if query:
        latest_foods = latest_foods.filter(name__icontains=query)  # Apply search filter

    if sort_by:
        latest_foods = latest_foods.order_by(sort_by)  # Apply sorting

    return render(request, 'food_list.html', {
        'latest_foods': latest_foods,
        'query': query,
        'sort_by': sort_by,
        'category_id': category_id #if isinstance(category_id, int) else None  # Pass category_id safely
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

@login_required
def order_history(request):
    user_orders = orders.objects.filter(student=request.user).order_by('-order_date')
    
    order_data = []
    for order in user_orders:
        order_items = OrderItems.objects.filter(orders=order)
        total_price = sum(item.price for item in order_items)  # Calculate total for each order
        order_data.append({
            'order': order,
            'items': order_items,
            'total_price': total_price  # Include total price
        })

    return render(request, 'order_history.html', {'order_data': order_data})
