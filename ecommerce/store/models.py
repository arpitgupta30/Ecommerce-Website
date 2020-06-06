from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200, null = True)
    price = models.DecimalField(max_digits = 7, decimal_places=2)
    digital = models.BooleanField(default=False, null = True, blank = False)
    image = models.ImageField(null = True, blank = True)



    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except: 
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank = True, null = True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        items = self.orderitem_set.all()
        for item in items:
            if not item.product.digital:
                shipping = True
                break
        return shipping
    
    @property
    def get_total_items(self):
        items = self.orderitem_set.all()
        total = 0
        for item in items:
            total+=item.quantity
        return total

    @property
    def get_total_price(self):
        items = self.orderitem_set.all()
        total_price = 0
        for item in items:
            total_price+=item.get_total
        return total_price


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default=0, blank=True, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.quantity*self.product.price
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null = True)
    address = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    state = models.CharField(max_length = 200, null = True)
    zipcode = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address