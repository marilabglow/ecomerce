"""Ecommercepro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import search
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop.views import *
from django.conf.urls import include 


'''urlpatterns = [ 
    path('search', SearchResultsView.as_view(), name='search_results'),
]'''

urlpatterns = [
    #path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('', interface, name = "interface"),
    path('search', search, name = "search"),  
    # Cart related urls:-
    path('cart/<pk>', add_cart, name = "add_cart"), 
    path('Show_cart', Show_cart, name = 'Show_cart'), 
    path('Cart_remove/<id>', Cart_remove, name = "Car_remove"),
    #path('Orderedby/<id>', Orderedby, name = "Orderedby"), #----saparate_cart prodct get url-----
    path('Orderedby', Orderedby, name = "Orderedby"),  
    path('addquantity/<id>', addquantity, name = "addquantity"), 
    path('Cancel_order/<id>',Cancel_order, name = "Cancel_order" ),
    #path('cancel_all_order/<id>', cancel_all_order, name = 'cancel_all_order'), 
    path('Orderhistory', Orderhistory, name = 'Orderhistory'),   
    # Login/register/logout/password's_Path
    path("login", login, name = "login"),
    path('Logout', Logout, name = 'Logout'), 
    path('register', Register, name = 'register'), 
    #Wish rlated urls:-
    path('wish/<pk>', add_wish, name = "add_wish"),
    path('Show_wish', Show_wish, name = 'Show_wish'), 
    path('wishremove/<id>', wish_remove, name = "wish_remove"),
    # json urls
    path('product_api', product_api, name = 'product_api'), 
    path('cart_api', cart_api, name = 'cart_api'), 
    path('Order_api', Order_api, name = 'Order_api'), 
    
]
# image url to share
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)


