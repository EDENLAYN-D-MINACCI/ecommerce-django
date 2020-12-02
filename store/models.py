from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def email_validation_function(value):
    validator = EmailValidator()
    validator(value)
    return value  



class Customer(models.Model): # OneToOne relationship, a user can only have one customer and vice versa
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, blank=True, validators=[email_validation_function])
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
    # the value that shows up in the admin panel 
    def __str__(self):
        return self.name 


class ProductCategories(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Product(models.Model):
    category = models.ForeignKey(ProductCategories, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
      if self.image:
           return self.image.url
      else:
           return '/static/image/default-product.png'


class Order(models.Model): # ManyToOne relationship, a customer can have multiple orders
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # set the customer value to null if deleted
    complete = models.BooleanField(default=False)
    date_complete = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def getCartTotal(self):
        orderItems = self.orderitem_set.all()
        return float(sum([item.getTotal for item in orderItems]))

    @property
    def getCartItemNumber(self):
        orderItems = self.orderitem_set.all()
        return sum([item.quantity for item in orderItems])
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True) 
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    name = models.CharField(max_length=200)
    taken_by = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    @property
    def getTotal(self):
        return self.product.price * self.quantity


