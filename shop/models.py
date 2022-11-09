from email.policy import default
from django.db.models import *
from datetime import datetime
from django.contrib import admin

#>>>>>>>>>>>>>>MODEL STATUS CHOISCES<<<<<<<<<<<<<<<<<<<<
# Order
SUCCESS = 1
PENDING = 2
FAILED = 0
ORDER_STATUS = (
    (SUCCESS, 'success'), 
    (PENDING, 'pending'), 
    (FAILED, 'cancel')
)

# Cart
NEWORDER = 1
OLDORDER = 2
CANCEL = 3
NOTORDER = 0
CART_STATUS = (
    (NEWORDER, 'new order'), 
    (OLDORDER, 'old order'), 
    (NOTORDER, 'not order'), 
    (CANCEL, 'cancel order')
)

# product
ADDWISH = 1
ADDCART = 2
NOTADDED = 0
PRODECT_STATUS = (
    (ADDWISH, 'added_wish'), 
    (ADDCART, 'added_cart'), 
    (NOTADDED, 'not_added')
)

#product_stocks
STOCKAVAILABLE = False
STOCKANOTVAILABLE = True
PRODECT_STOCK = (
    (STOCKAVAILABLE, 'stockavailable'), 
    (STOCKANOTVAILABLE, 'stockanotvailable')
)
#Payment options:
CASHONDELIVERY= False
Gpay= True

class DateTimeUpdate(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# Create your models here.
class product(Model):
    name = CharField(max_length=150)
    model = CharField(max_length=150)
    image = ImageField(upload_to = "Pictures")
    category = CharField(max_length=150)
    brand = CharField(max_length=150)
    price = DecimalField(max_digits=10, decimal_places=2,)
    stock = BooleanField(default=False, help_text = "0-Show, 1-Hidden", choices = PRODECT_STOCK)
    added = IntegerField(default = 0, choices = PRODECT_STATUS) # 1.added_wish, 2.added_cart, 3.not_added
    def __str__(self):
        return self.name


class Cart(DateTimeUpdate):
    customer = CharField(max_length = 30)  
    image = ImageField(upload_to = "cart_img")
    name = ForeignKey(product, on_delete = CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField(default = 1) 
    order = BooleanField(default=False, help_text = "0-Add, 1-Remove")
    order_status = IntegerField(default = 0, choices = CART_STATUS)# 0.not_order, 1.new_order, 2.old_order, 3.cancel_order  
    #date =DateTimeField(default=datetime.now, blank=True)

def tax():
    return (18/100)
class Orderby(DateTimeUpdate):
    customer = CharField(max_length = 30) 
    ordered_things =  ManyToManyField(Cart)
    order_status = IntegerField(default = 2, choices = ORDER_STATUS)
    tax = FloatField(default = tax())
    #date =DateTimeField(default=datetime.now, blank=True)
    '''
    1.success, 2.bending, 0.cancel
    '''
class Wishlist(DateTimeUpdate):
    customer = CharField(max_length = 30)  
    image = ImageField(upload_to = "cart_img")
    name = ForeignKey(product, null=True, on_delete = CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField(default = 1) 
    order = BooleanField(default=False,help_text = "0-Add, 1-Remove") 

# Create your models here.
