from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [

path('index/', views.index, name='index'),
path('', views.home, name='home'),
path('layout/', views.layout, name='layout'),
# path('feedback/', views.feedback, name='feedback'),
path('bill/', views.bill, name='bill'),

path('food_list/<str:meal_type>/', views.foodbycategory, name='foodbycategory'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
