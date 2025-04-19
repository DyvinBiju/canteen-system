from django.urls import path
from .views import signup_view, login_view, logout_view, home, index, profile_view
from django.conf.urls.static import static
from . import views
from .views import add_to_cart, view_cart, remove_from_cart, checkout
from django.conf import settings
from .views import signup_view, login_view, logout_view, home, index, profile_view
from .views import increase_quantity, decrease_quantity
urlpatterns = [

path('', home, name='home'),   
path('about/', views.about, name='about'),    
path('testimonial/', views.testimonial, name='testimonial'),        
path('signup/', signup_view, name='signup'), 
path('login/', login_view, name='login'),    
path('logout/', logout_view, name='logout'), 
path('profile/', profile_view, name='profile'),
path('profile/', views.profile_view, name='profile'),
path('profile/edit/', views.edit_profile, name='edit_profile'),
path('profile/upload-picture/', views.upload_profile_picture, name='upload_profile_picture'),
path('index/', views.index, name='index'),
path('', views.home, name='home'),
path('layout/', views.layout, name='layout'),
path('bill/', views.bill, name='bill'),
path('food_list/', views.food_list, name='food_list'),
path('view_cart/', views.view_cart, name='view_cart'),
path('remove_from_cart/<int:food_id>/', remove_from_cart, name='remove_from_cart'),
path('checkout/', checkout, name='checkout'),
path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
path('order_history/', views.order_history, name='order_history'),
path('increase-quantity/<str:food_id>/', increase_quantity, name='increase_quantity'),
path('decrease-quantity/<str:food_id>/', decrease_quantity, name='decrease_quantity'),
path('feedback/<int:order_id>/', views.give_feedback, name='give_feedback'),
path('profile/delete-picture/', views.delete_profile_picture, name='delete_profile_picture'),
path('profile/delete-account/', views.delete_account, name='delete_account'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
