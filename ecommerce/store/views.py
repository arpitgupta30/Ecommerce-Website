from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from . utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request):
    products = Product.objects.all()
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_total = data['cart_total']
    
    context = {'products': products,
                'cart_total': cart_total}
    return render(request, 'store/store.html', context)

def cart(request):
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_total = data['cart_total']
        
    context = {'items': items,
                'order': order,
                'cart_total':cart_total    
                }
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_total = data['cart_total']

    context = {'items': items,
                'order': order,    
                'cart_total': cart_total,
                }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    
    product = Product.objects.get(id = productId)
    
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity-1
    orderItem.save()


    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse("Data was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        

    else:
        customer, order = guestOrder(request, data)      

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if(total == order.get_total_price):
        order.complete = True
    
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer= customer,
            order= order, 
            address= data['shipping']['address'],
            city= data['shipping']['city'],
            state= data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )

    return JsonResponse("Payment was completed", safe = False)