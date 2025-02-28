from django.urls import path

from . import views

urlpatterns = [

path('index/', views.index, name='index'),
path('', views.home, name='home'),
path('layout/', views.layout, name='layout'),
path('food_list/', views.food_list, name='food_list'),
path('feedback/', views.feedback, name='feedback'),
path('bill/', views.bill, name='bill'),

]