from django.urls import path
from shop import views
from shop.views import *

urlpatterns = [

    path('products/', views.products, name='products'),
    path('search', views.Search, name='search'),
    path('addtocart', views.addtocart, name='addtocart'),
    path("login", login, name = "login"),
    path('Logout', Logout, name = 'Logout'), 
    path('register', register, name = 'register'), 

]
