from django.shortcuts import render
from . models import OrderItems
from django.db.models import Sum

# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def layout(request):
    return render(request,'layout.html')

def food_list(request):
    return render(request,'food_list.html')

def feedback(request):
    return render(request,'feedback.html')

def bill(request):
    bill_set=OrderItems.objects.all()
    print(bill_set)

    # total_price = OrderItems.objects.aggregate(total=Sum('price'))['total']
    # print(total_price)
    return render(request,'bill.html',{'bill_data':bill_set})
