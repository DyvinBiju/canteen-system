from django.urls import path

from . import views

urlpatterns = [

path('fdgf', views.index, name='index'),
path('', views.home, name='home'),
path('layout/', views.layout, name='layout'),
path('food_list/', views.food_list, name='food_list'),

]