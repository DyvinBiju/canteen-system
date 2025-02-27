from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def layout(request):
    return render(request,'layout.html')

def food_list(request):
    return render(request,'food_list.html')