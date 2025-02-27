from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def layout(request):
    return render(request,'layout.html')

def foodlist(request):
    return render(request,'foodlist.html')