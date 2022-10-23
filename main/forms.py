from django.forms import *
from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', )


class InvestorForm(ModelForm):
    class Meta:
        model = Investor
        fields = '__all__'
        exclude = ['user']

class ProductForm(ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'
        labels = {
            'qty': 'Quantity',
            'desc': 'Description',
            'sku': 'SKU',
            'price': 'Price',
        }
        help_texts = {}
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Enter product name'
            }),
            'sku': TextInput(attrs={
                'placeholder': 'Enter a unique SKU/identifier',
                }),
            'desc': Textarea(attrs={
                'placeholder': 'Enter product description',
                'rows': 2,
            }),
            'qty': NumberInput(attrs={
                'placeholder': 'Enter quantity',
            }),
            'price': NumberInput(attrs={
                'placeholder': 'Enter regular price ',
            })
            }


class ProductUnitForm(ModelForm):
    class Meta:
        model = ProductUnit
        fields = '__all__'
        exclude = ['product_model', 'owner','price_sold', 'profit', 'status', 'sold_at']


class ProductUnitUpdateForm(ModelForm):
    class Meta:
        model = ProductUnit
        fields = '__all__'
        exclude = ['product_model', 'sold_at', 'price_sold', 'profit']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

