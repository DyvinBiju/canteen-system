from django.urls import path
from django.conf.urls.static import static
from . import views
from .views import add_to_cart, view_cart, remove_from_cart, checkout
from django.conf import settings

urlpatterns = [

path('index/', views.index, name='index'),
path('', views.home, name='home'),
path('layout/', views.layout, name='layout'),
# path('feedback/', views.feedback, name='feedback'),
path('bill/', views.bill, name='bill'),

path('food_list/<str:meal_type>/', views.foodbycategory, name='foodbycategory'),

path('add_to_cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
path('view_cart/', views.view_cart, name='view_cart'),
path('remove_from_cart/<int:food_id>/', remove_from_cart, name='remove_from_cart'),
path('checkout/', checkout, name='checkout'),
path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
