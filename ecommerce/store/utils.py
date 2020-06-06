import json
from . models import *

def cookieCart(request):
    try:
        cart  = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print("Cart:", cart)
    items = []
    order = {'get_total_items': 0, 'get_total_price': 0, 'shipping': False}
    cart_total = order['get_total_items']
    
    for i in cart:
        try:
            cart_total+=cart[i]['quantity']
            
            product = Product.objects.get(id = i)
            total = product.price*cart[i]['quantity']
            
            order['get_total_items']+=cart[i]['quantity']
            order['get_total_price']+=total

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                    },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'items': items,'order': order,'cart_total':cart_total,} 


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cart_total = order.get_total_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cart_total = cookieData['cart_total']
    return {'items': items,'order': order,'cart_total':cart_total,}


def guestOrder(request, data):
    print("User not logged in")
    print("Cookies: ", request.COOKIES)
    
    name = data['form']['name']
    email = data['form']['email']
    
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, complete = False)

    for item in items:
        
        product = Product.objects.get(id = item['product']['id'])
        orderItem = OrderItem.objects.create(product = product, order = order, quantity = item['quantity'])
    
    return customer, order