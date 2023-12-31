from django.shortcuts import get_object_or_404, redirect, render
from cart_app.models import Cart, CartItem

from product_app.models import Product, Variation

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


    
       
@login_required(login_url = 'log_in')
def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            # print(key,value)
            
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                # print(variation)
            except:
                pass
            
        
    try:
        
        cart = Cart.objects.get(user=request.user,cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        user=request.user
        cart = Cart.objects.create(
            user=user,
            cart_id = _cart_id(request)
        )
    cart.save()
    
    
    is_cart_item_exist= CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        
        existing_variation_list=[]
        id =[]
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            
            id.append(item.id)
            
        # print(existing_variation_list)
            
        if product_variation in existing_variation_list:
            index=existing_variation_list.index(product_variation)  
            item_id=id[index]
            item=CartItem.objects.get(product=product, id=item_id)
            item.quantity+=1
            item.save()
        else:
            item= CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            # cart_item.quantity +=1
            item.save()
    else :
        cart_item = CartItem.objects.create(
            product  = product,
            quantity = 1,
            cart     = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    # return HttpResponse (cart_item.quantity)
    # exit()
    return redirect ('cart')
    
       



def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =  _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
        
    return redirect('cart')

def remove_cart_btn(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =  _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    
    
    
    
    

@login_required(login_url = 'log_in')
def cart(request, total=0, quantity=0, cart_item= None):
    cart_items = []
    tax=0
    grand_total=0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart , is_active=True)
        for cart_item in cart_items:
            total+=  (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (5*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass
    
        
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render (request, 'cart/cart.html',context)





@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0


        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass 

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/checkout.html', context)



# @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass 

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'cart/checkout.html', context)