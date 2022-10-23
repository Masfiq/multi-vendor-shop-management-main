from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=25, unique=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=500)
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    AGE_GROUP_CHOICES = [
        ('Young', 'Young'),
        ('Adult', 'Adult'),
        ('Old', 'Old'),
    ]
        
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=25, unique=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=500, default="Dhaka, BD")

    def __str__(self):
        return self.name

class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    balance = models.DecimalField(decimal_places=3, max_digits=30)
    profit = models.DecimalField(decimal_places=3, max_digits=25)
    profit_lifetime = models.DecimalField(decimal_places=3, max_digits=30)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
        
    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sku = models.CharField(max_length=200, unique=True)
    desc = models.TextField(null=True, blank=True)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=18)
    price = models.DecimalField(decimal_places=2, max_digits=18)
    categories = models.ManyToManyField(Category, related_name='products')

    
    def __str__(self):
        return self.name


class ProductUnit(models.Model):
    product_model = models.ForeignKey(ProductModel, related_name='units', on_delete=models.CASCADE)
    serial = models.CharField(max_length=30, unique=True)
    short_description = models.CharField(max_length=256, null=True, blank=True)
    store = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    owner = models.ForeignKey(Investor, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    price_sold = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=18)
    profit = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=18)

    created_at = models.DateTimeField(auto_now_add=True)
    sold_at = models.DateTimeField(null=True)

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available',
    )

    def __str__(self):
        return f' {self.product_model.name} ({self.serial})'


class Order(models.Model):
    customer = models.ForeignKey(Customer, default=1, on_delete=models.SET_DEFAULT)
    gross = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    STATUS_CHOICES = [
        ('PAID', 'PAID'),
        ('UNPAID', 'UNPAID'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PAID')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_discount(self):
        return self.total - self.gross

    def __str__(self):
        return f'Order # {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=18)
    discount = models.DecimalField(decimal_places=2, max_digits=18)
    
    def __str__(self):
        return self.product_model.name

class OrderUnit(models.Model):
    item = models.ForeignKey(OrderItem, related_name='units', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_model.name

