from django.urls import path
from .views import signup_view, login_view, logout_view, home, index, profile_view

urlpatterns = [
    path('', home, name='home'),        
    path('index/', index, name='index'),
    path('signup/', signup_view, name='signup'), 
    path('login/', login_view, name='login'),    
    path('logout/', logout_view, name='logout'), 
    path('profile/', profile_view, name='profile'),
]
