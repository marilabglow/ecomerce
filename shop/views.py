from contextlib import redirect_stderr
from ssl import create_default_context
from unicodedata import name
from django.shortcuts import render, redirect
from shop.models import *
from django.http import *
# genaricView_moduels:-
from django.db.models import Q
# message:-
from django.contrib import messages
# login__logout _authenticate moduels:-
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as authlogin, logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
# only_allowed_login person:-
from django.contrib.auth.decorators import login_required
from datetime import *
#jason_related_moduel:
from django.core.serializers import *
import json




#------------------------------------------------------

# all_products & Home_page

def interface(request):
    opj = product.objects.all()
    return render (request, "interface.html",{"opj":opj})
# --------------------------------------------------------

# search_box

def search(request):
  
    opj = product.objects.filter((Q(brand = request.POST.get("search")) | Q(category = request.POST.get("search")) | Q(name = request.POST.get("search"))) & Q(stock = 0))
    return render (request, 'interface.html', {'opj': opj})
   # search_list = list(opj.values())
    #return JsonResponse(search_list,safe=False)
# --------------------------------------------------------

# add_to_cart products(tb_added):-
@login_required
def add_cart(request, pk):
    if request:
        
        opj = product.objects.get(id = pk)
        opj.added = 2
        opj.save()

        addCart_value, success_created = Cart.objects.get_or_create(
            name = opj,
            price = opj.price,
            image = opj.image, 
            order = False, 
            customer = request.user 
               
        )
        
        if success_created:
            messages.info(request,'The item was added to your Cart')
        else:
            messages.info(request,'The item was already in your Cart')   
        return redirect("interface")
    else:
        return HttpResponse("<h1>Prodects Not Added to Cart</h1>")
# --------------------------------------------------------

# Cart_Show :-
@login_required
def Show_cart(request):
    opj = Cart.objects.filter(
        order = False, 
        customer = request.user
        )
    return render (request, 'Cart_view.html', {'opj': opj})
    #show_cart_list = list(opj.values())
    #return JsonResponse(show_cart_list,safe=False)

# cart_items_remove:-
@login_required
def Cart_remove(request, id):
    if request:
        opj = Cart.objects.get(id = id)

        opj1 = product.objects.get(id = opj.name.id)
        opj1.added = 0
        opj1.save()

        opj.delete()
    return redirect("Show_cart")    

# cart quantity_add:-
@login_required
def addquantity(request, id):
    opj = Cart.objects.get(id = id)
    #opj1 = request.POST.get('quantity')
    opj.quantity = request.POST.get('quantity')
    opj.save()
    return redirect('Show_cart')
#------------------------------------------------------

# login_Page:-

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    
        if user is not None:
            if user.is_active:
                authlogin(request, user)
                return redirect('interface')
        else:
            return HttpResponse("Try Again")
    
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    


#------------------------------------------------------

# logout_:-
@login_required
def Logout(request):
    logout(request)
    return redirect('interface')    
#------------------------------------------------------

# register_page:-

def Register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password)
            authlogin(request, user)
            return redirect('interface')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form}) 


#------------------------------------------------------

@login_required
def Orderedby(request):
    """
    product's added to order Table 
    """
    ak = product.objects.all()
    ak.update(added = 0) # product added staus change 

    if request.method == 'POST' : 
        opj = Cart.objects.filter(
            customer = request.user, 
        )
        opj2= Orderby.objects.create(
            customer = request.user, 
        )      
        opj2.ordered_things.add(
            *Cart.objects.filter(Q(customer = request.user) & Q(order = False))
        )
        opj.update(order = True)
        #return redirect('/')

    #>>>> order_view code <<<:-    
    if request:
        opj2= Orderby.objects.latest(
            'ordered_things__id' 
        )
        
        opj1 = opj2.ordered_things.filter(order_status = 0) # m3m key
        total = opj2.ordered_things.filter(order_status = 0).aggregate(p_q = Sum(F('price') * F('quantity')))# p_q => product & quantity 
        count = opj1.count()
        tax = int(total['p_q']) * opj2.tax
        #print(int(tax))
        contaxt = {
            'opj1':opj1, # order's m2m_cart
            'opj2':opj2, # order tb
            'total':total['p_q']+ int(tax),
            'tax':int(tax),  
            'count':count, 
            
            
        }
    return render(request, "orderview_page.html" , contaxt)
# order_cancel:
def Cancel_order(request, id):
    if request.method == "POST":
        opj_cart = Cart.objects.filter(Q(id = id))
        opj_cart.update(order_status = 3) # Cart cancel
        opj_cart.update(updated_at = datetime.now())
        return redirect('Orderedby')


#order_history
def Orderhistory(request):
    #if request.method == "POST":
        opj = Cart.objects.filter(Q(customer = request.user) & Q(order_status = 1) | Q(order_status = 2) | Q(order_status = 3)).order_by('updated_at')
        contaxt = { 
            'opj':opj
        }
        print('opj2', opj)
        return render(request, 'orderhistory.html', contaxt)
        #show_order_history = list(opj.values())
        #return JsonResponse(show_order_history,safe=False)
#------------------------------------------------------

# add_to_wish;-

def add_wish(request, pk):
    if request:
        
        opj = product.objects.get(id = pk)
        opj.added = 1
        opj.save()

        addCart_value, success_created = Wishlist.objects.get_or_create(
            name = opj,
            price = opj.price,
            image = opj.image, 
            order = False, 
            customer = request.user 
               
        )
       
        if success_created:
            #messages.info(request,'The item was Already in your Cart')
            messages.info(request,'The item was added to your WishList')
        else:
            messages.warning(request,'The item was Already to your WishList')    
        return redirect("interface")
    else:
        return HttpResponse("<h1>Prodects Not Added to Cart</h1>")         

# wish_Show :-

def Show_wish(request):
    
    opj = Wishlist.objects.filter(
        order = False, 
        customer = request.user
        )
    return render (request, 'wish.html', {'opj': opj})
    #wish_list = list(opj.values())
    #return JsonResponse(wish_list,safe=False)

# wish_remove:-
def wish_remove(request, id):
    '''
    >> remove your separate wish product's <<
    '''
    opj = Wishlist.objects.get(id = id)

    opj1 = product.objects.get(id = opj.name.id)
    opj1.added = 0
    opj1.save()
    #messages.warning(request,'The item was Already to your WishList')    
    opj.delete()
    return redirect("Show_wish") 

#------------------------------------------------------


def product_api(request, prety = True):
    Product_data = product.objects.all()
    product_jn_convert = serialize('json' ,Product_data, fields = (
        'name', 'model', 'image', 'category', 'brand', 'price', 'stock', 
        'added'
    ))
    product_jn_convert_f = json.dumps(json.loads(product_jn_convert), indent=4)
    #print(product_jn_convert_f)
    return HttpResponse(product_jn_convert_f)



def cart_api(request, prety = True):
    Cart_data = Cart.objects.all()
    Cart_jn_convert = serialize('json' ,Cart_data, fields = (
        'customer', 'image', 'name', 'category', 'price', 'quantity', 'order', 
        'order_status'
    ))
    Cart_jn_convert_f = json.dumps(json.loads(Cart_jn_convert), indent=4)
    #print(Cart_jn_convert_f)
    return HttpResponse(Cart_jn_convert_f)
    

def Order_api(request, prety = True):
    Order_data = Cart.objects.all()
    Order_jn_convert = serialize('json' ,Order_data, fields = (
        'customer', 'ordered_things', 'order_status', 'tax'
    ))
    Order_jn_convert_f = json.dumps(json.loads(Order_jn_convert), indent=4)
    #print(Order_jn_convert_f)
    return HttpResponse(Order_jn_convert_f)

    


      
