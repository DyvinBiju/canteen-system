from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback, FoodItems,orders,OrderItems
from .models import Category
from datetime import datetime
from django.urls import reverse
from django.http import FileResponse
from reportlab.pdfgen import canvas # type: ignore
import io
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.lib import colors # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from .models import UserProfile
from django.db.models import Avg
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re




# Create your views here.

def index(request):
    return render(request,'index.html', {})

def home(request):
    # query category
    categories = Category.objects.all()
    return render(request,'home.html',{'categories':categories})
    

def about(request):
    return render(request,'about.html',)

def testimonial(request):
    return render(request,'testimonial.html',)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html', {'form_data': request.POST})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Enter a valid email address.")
            return render(request, 'signup.html', {'form_data': request.POST})

        if len(password) < 8 or len(password) > 12:
            messages.error(request, "Password must be between 8 and 12 characters.")
            return render(request, 'signup.html', {'form_data': request.POST})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'form_data': request.POST})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html', {'form_data': request.POST})

        User.objects.create_user(username=username, email=email, password=password)
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
            messages.success(request, "Login successful!")
            return redirect('login')  # Redirect to login so the message shows briefly
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages

@login_required
def profile_view(request):
    # Fetch the user's profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Render the profile page
    return render(request, 'profile.html', {'user_profile': user_profile})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile

@login_required
def profile_view(request):
    """
    View to display the user's profile.
    """
    user_profile = UserProfile.objects.filter(user=request.user).first()  # Fetch without creating
    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def edit_profile(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('edit_profile')

        user.username = username
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = email

        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']

        user.save()
        user_profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('edit_profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile})


@login_required
def delete_profile_picture(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        if profile.profile_picture:
            profile.profile_picture.delete()
            profile.save()
        return JsonResponse({'success': True})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('login')  # Or your homepage










@login_required
def upload_profile_picture(request):
    """
    View to handle uploading a profile picture.
    """
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_picture = profile_picture
            user_profile.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.warning(request, 'No file was uploaded.')
        return redirect('profile')



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



def food_list(request):
    category_id = request.GET.get('category_id')
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    page_number = request.GET.get('page')

    latest_foods = FoodItems.objects.all()

    if category_id:
        latest_foods = latest_foods.filter(category_id=category_id)

    if query:
        latest_foods = latest_foods.filter(name__icontains=query)

    # Annotate average rating
    latest_foods = latest_foods.annotate(avg_rating=Avg('feedback__rating'))

    # Sorting logic
    if sort_by == 'name':
        latest_foods = latest_foods.order_by(Lower('name'))  # Case-insensitive sort
    elif sort_by == 'avg_rating':
        latest_foods = latest_foods.order_by('-avg_rating')
    elif sort_by in ['price', 'created_at', 'f_stock']:
        latest_foods = latest_foods.order_by(sort_by)

    # Pagination
    paginator = Paginator(latest_foods, 8)
    page_obj = paginator.get_page(page_number)

    return render(request, 'food_list.html', {
        'latest_foods': page_obj,
        'query': query,
        'sort_by': sort_by,
        'category_id': category_id,
        'page_obj': page_obj
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
    request.session['cart_count'] = len(cart)
    messages.success(request,f"{food_item.name} successfully added to cart")

    category_id = request.POST.get('category_id')  # Get category_id from URL
    if category_id:
        return redirect(f"{reverse('food_list')}?category_id={category_id}")
    return redirect('food_list')  # Default redirect if no category_id



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
    food_item = get_object_or_404(FoodItems, id=food_id)
    if str(food_id) in cart:
        del cart[str(food_id)]

    request.session['cart'] = cart
    request.session['cart_count'] = len(cart)
    messages.success(request,f"{food_item.name} successfully removed from cart")

    return redirect('view_cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    # Create Order and save to database
    order = orders.objects.create(student=request.user)

    # Prepare PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add title
    elements.append(Paragraph("<strong>Delfood</strong>", styles['Title']))
    # elements.append(Paragraph(" Holy Cross Collage Cherpunkal,Kottayam,Kerala", styles['Normal']))
    # elements.append(Paragraph("Phone: +91 XXXXXXXXXX", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Add customer details
    elements.append(Paragraph(f"<b>Customer Name:</b> {request.user.username.upper()}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # Table Headers
    data = [["Item Name", "Quantity", "Price (Rs)", "Total (Rs)"]]
    total_price = 0

    for food_id, item in cart.items():
        food_item = FoodItems.objects.get(id=food_id)

        # Save order items in database
        OrderItems.objects.create(
            food=food_item,
            orders=order,
            quantity=item['quantity'],
            price=food_item.price * item['quantity']
        )

        item_total = food_item.price * item['quantity']
        total_price += item_total

        data.append([item['name'], item['quantity'], f"{item['price']}", f"{item_total}"])

    # Add total row
    data.append(["", "", "Grand Total", f"Rs {total_price}"])

    # Create table with styles
    table = Table(data, colWidths=[200, 80, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Footer
    elements.append(Paragraph("Thank you for ordering with us!", styles['Italic']))
    elements.append(Paragraph("Visit again!", styles['Italic']))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    # Clear the cart after order completion
    request.session['cart'] = {}
    request.session['cart_count'] = 0
    request.session.modified = True

    # Return PDF as response
    response = FileResponse(buffer, as_attachment=True, filename=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    return response

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

def increase_quantity(request, food_id):
    cart = request.session.get('cart', {})

    if food_id in cart:
        cart[food_id]['quantity'] += 1
        cart[food_id]['total'] = cart[food_id]['quantity'] * cart[food_id]['price']
    
    request.session['cart'] = cart  # Save updated cart in session
    return redirect('view_cart')

def decrease_quantity(request, food_id):
    cart = request.session.get('cart', {})

    if food_id in cart:
        if cart[food_id]['quantity'] > 1:
            cart[food_id]['quantity'] -= 1
            cart[food_id]['total'] = cart[food_id]['quantity'] * cart[food_id]['price']
        else:
            del cart[food_id]  # Remove item if quantity reaches 0

    request.session['cart'] = cart  # Save updated cart in session
    return redirect('view_cart')


@login_required
def give_feedback(request, order_id):
    user = request.user
    order = get_object_or_404(orders, id=order_id, student=user)

    ordered_items = OrderItems.objects.filter(orders=order)
    purchased_items = FoodItems.objects.filter(
        id__in=ordered_items.values_list('food_id', flat=True)
    ).distinct()

    feedback_dict = {
        feedback.food_item.id: feedback.rating
        for feedback in Feedback.objects.filter(student=user, food_item__in=purchased_items)
    }

    items_with_ratings = []
    for item in purchased_items:
        items_with_ratings.append({
            'item': item,
            'rating': feedback_dict.get(item.id, 0)
        })

    if request.method == 'POST':
        for entry in items_with_ratings:
            item = entry['item']
            rating = request.POST.get(f'rating_{item.id}')
            if rating:
                Feedback.objects.update_or_create(
                    student=user,
                    food_item=item,
                    defaults={'rating': int(rating)}
                )
        return redirect('order_history')  # or your desired success page

    return render(request, 'feedback.html', {
        'items_with_ratings': items_with_ratings
    })

