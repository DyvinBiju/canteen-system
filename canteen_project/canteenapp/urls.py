from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [

path('fdgf', views.index, name='index'),
path('', views.home, name='home'),
path('layout/', views.layout, name='layout'),
path('food_list/', views.food_list, name='food_list'),
path('food_latest/<str:food_name>/', views.food_detail, name='food_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
