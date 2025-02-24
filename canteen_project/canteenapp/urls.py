from django.urls import path

from . import views

urlpatterns = [

path('fdgf', views.index, name='index'),
path('', views.home, name='home'),

]