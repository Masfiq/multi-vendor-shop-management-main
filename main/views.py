from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
import decimal
import datetime
from django.utils import timezone

from .decorators import staff_only, admin_only
from .forms import *
from .models import *
from .filters import *



@login_required(login_url='/login/')
@staff_only
def index(request):
    order_list = Order.objects.all()
    customer_list = Customer.objects.all()[:5]
    product_list = ProductModel.objects.all().annotate(instock=Count('units', filter=Q(units__status='Available'))).order_by('instock')
    pending_order_count = Order.objects.filter(status='UNPAID').count()
    paid_order_count = Order.objects.filter(status='PAID').count()
    
    stock_warning = False
    for product in ProductModel.objects.all():
        if product.units.count() < 5:
            stock_warning = True
            break

    product_stock = ProductUnit.objects.filter(status='Available').count()
    context = {
        'counts': {
            'product': product_stock,
            'unpaid_order': pending_order_count,
            'paid_order': paid_order_count,
        },
        'products': product_list[:5],
        'customers': customer_list,
        'orders': order_list[:5],
        'stockwarning': stock_warning,
    }
    return render(request, 'main/index.html', context=context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'main/login.html')


@login_required(login_url='/login/')
def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
@staff_only
def products(request):
    prods = ProductModel.objects.all().annotate(instock=Count('units', filter=Q(units__status='Available'))).order_by('instock')
    products_filter = ProductFilter(request.GET, queryset=prods)
    prods = products_filter.qs
    context = {
        'products': prods,
        'prodfilter': products_filter,
    }
    return render(request, 'main/products.html', context=context)


@login_required(login_url='/login/')
@staff_only
def product(request, pk):
    return render(request, 'main/product.html')


@login_required(login_url='/login/')
@staff_only
def new_product(request):
    productform = ProductForm()
    context = {
        'productform' : productform,
    }
    if request.method == 'POST':
        productform = ProductForm(request.POST)
        if productform.is_valid():
            productform.save()
            return redirect('products')

    return render(request, 'main/new_product.html',  context=context)

@login_required(login_url='/login/')
@staff_only
def customers(request):
    customers_list = Customer.objects.all()
    context = {
        'customers':customers_list
    }
    return render(request, 'main/customers.html', context=context)

@login_required(login_url='/login/')
@staff_only
def suppliers(request):
    suppliers_list = Supplier.objects.all()
    context = {
        'suppliers': suppliers_list
    }
    return render(request, 'main/suppliers.html', context=context)


@login_required(login_url='/login/')
@staff_only
def new_supplier(request):
    supplier_form = SupplierForm()
    
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier_form.save()
            return redirect('suppliers')

    context = {
        'supplierform': supplier_form,
    }
    return render(request, 'main/new_supplier.html', context=context)



@login_required(login_url='/login/')
@admin_only
def investors(request):
    investor_list = Investor.objects.all().annotate(instock=Count('products', filter=Q(products__status='Available'))).order_by('instock')
    context = {
        'investors': investor_list,
        'profit_share': settings.PROFIT_SHARE,
    }
    return render(request, 'main/investors.html', context=context)


@login_required(login_url='/login/')
@admin_only
def investor(request, pk):
    investor = get_object_or_404(Investor, id=pk)
    products = investor.products.filter(status='Available')
    
    stock_price = 0
    for product in products:
        stock_price += product.product_model.purchase_price

    cash_in_hand = investor.balance - stock_price

    context = {
        'investor': investor,
        'products': products[:10],
        'stock_price': stock_price,
        'cash_in_hand': cash_in_hand,
    }
    return render(request, 'main/investor_dashboard.html', context)

@login_required(login_url='/login/')
@admin_only
def new_investor(request):
    userform = UserForm()
    form = InvestorForm()

    if request.method == 'POST':
        userform = UserForm(request.POST)
        form = InvestorForm(request.POST)
        if userform.is_valid() and form.is_valid():
            user = userform.save()
            investor = form.save(commit=False)
            investor.user = user
            investor.save()
            return redirect('investors')

    context = {
        'userform': userform,
        'investorform': form,
    }
    return render(request, 'main/new_investor.html', context=context)


@login_required(login_url='/login/')
@admin_only
def update_profit_share(request):
    if request.method == 'POST':
        settings.PROFIT_SHARE = float(request.POST['profit_share'])
        return redirect('investors')
    return HttpResponseForbidden()


@login_required(login_url='/login/')
@admin_only
def release_profit(request):
    
    investors = Investor.objects.all()
    for investor in investors:
        investor.profit_lifetime += investor.profit
        investor.balance += investor.profit
        investor.profit = 0
        investor.save()
        
    return redirect('investors')


@login_required(login_url='/login/')
@staff_only
def customer(request, pk):
    return render(request, 'main/customer.html')


@login_required(login_url='/login/')
@staff_only
def new_customer(request):
    customerform = CustomerForm()
    if request.method == 'POST':
        customerform = CustomerForm(request.POST)

        if customerform.is_valid():
            customerform.save()
            return redirect('customers')
 
    context = {
        'customerform': customerform,
    }
    return render(request, 'main/new_customer.html', context)


@login_required(login_url='/login/')
@staff_only
def orders(request):
    orders_list = Order.objects.all()
    context = {
        'orders':orders_list.reverse()
    }
    return render(request, 'main/orders.html', context=context)


@login_required(login_url='/login/')
@staff_only
def order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.is_ajax():
        if request.method == 'POST':
            if 'paid' in request.POST:
                if request.POST.get('paid')=='true':
                    order.status = 'PAID'
                elif request.POST.get('paid')=='false':
                    order.status = 'UNPAID'
                order.save()
                return JsonResponse({'status': order.status})
            elif 'delete' in request.POST:
                if request.POST.get('delete')=='true':
                    Order.objects.get(id=pk).delete()
                    return JsonResponse({'message': 'deleted'})
   
    context = {
        'order': order,
    }
    return render(request, 'main/order.html', context=context)


@login_required(login_url='/login/')
@staff_only
def new_order(request):
    products = ProductModel.objects.all().annotate(num_units=Count('units', filter=Q(units__status='Available'))).filter(num_units__gt = 0)

    print(products)
    if request.is_ajax():
        data = {
            'message': 'sucessful',
            'products': list(products.values()),
        }
        return JsonResponse(data)
    

    customers = Customer.objects.all()
    context = {
        'products': products,
        'customers': customers,
    }
    if request.method == 'POST':
        customer_id = int(request.POST.get('customer'))
        products = request.POST.getlist('product[]')
        serials = request.POST.getlist('serials[]')
        discounts = request.POST.getlist('discount[]')
        quantities = request.POST.getlist('qty[]')
        amounts = request.POST.getlist('amount_value[]')
        gross = float(request.POST.get('gross_amount_value'))
        total = float(request.POST.get('net_amount_value'))

        if len(serials) != len(set(serials)):
            messages.add_message(request, messages.ERROR, 'You can not sell same product (serial) more then once!')
            return render(request, 'main/new_order.html', context=context)
        
        if len(products) != len(set(products)):
            messages.add_message(request, messages.ERROR, 'Please select only one product with all serials, Thanks!')
            return render(request, 'main/new_order.html', context=context)

        sumqty = 0
        for q in quantities:
            sumqty += int(q)
        if sumqty != len(serials): 
            messages.add_message(request, messages.ERROR, 'Unknown Error Occured! Please contact with software engineer')
            return render(request, 'main/new_order.html', context=context)
        
        # Create new order
        order = Order()
        order.customer = Customer.objects.get(id=customer_id)
        order.gross = gross
        order.total = total
        order.save()

        serial_index = 0
        for index, product_id in enumerate(products):
            product = ProductModel.objects.get(id=int(product_id))
            
            # Create new order item for each product
            order_item = OrderItem()
            order_item.order = order
            order_item.product_model = product
            order_item.discount = float(discounts[index])
            order_item.amount = float(amounts[index]) - float(discounts[index])
            order_item.save()

            qty = int(quantities[index])
            unit_discount = order_item.discount / qty

            for _ in range(qty):
                unit = ProductUnit.objects.filter(serial=serials[serial_index]).first()

                if unit.status == 'Sold':
                    messages.add_message(request, messages.ERROR, 'Can not sell a item that is already sold!')
                    return render(request, 'main/new_order.html', context=context)

                # Update product unit info
                unit.status = 'Sold'
                unit.price_sold = product.price - decimal.Decimal(unit_discount)
                unit.profit = unit.price_sold - product.purchase_price
                unit.sold_at = timezone.now()
                unit.save()

                # add profit to owner
                investor = unit.owner
                investor.profit += (unit.profit / 100) * decimal.Decimal(settings.PROFIT_SHARE)
                investor.save()

                # Create order unit
                order_unit = OrderUnit()
                order_unit.item = order_item
                order_unit.product = unit
                order_unit.save()

                serial_index += 1
            
        return redirect('orders')

    return render(request, 'main/new_order.html', context=context)


@login_required(login_url='/login/')
@staff_only
def categories(request):
    category_form = CategoryForm()
    categories = Category.objects.all()
    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    context = {
        'categoryform': category_form,
        'categories': categories,
    }
    return render(request, 'main/categories.html', context=context)


@login_required(login_url='/login/')
@staff_only
def stores(request):
    stores = Store.objects.all().annotate(instock=Count('products', filter=Q(products__status='Available'))).order_by('instock')
    store_form = StoreForm()
    
    if request.method == 'POST':
        store_form = StoreForm(request.POST)
        if store_form.is_valid():
            store_form.save()
            return redirect('stores')
    context = {
        'stores':stores,
        'storeform': store_form,
    }
    return render(request, 'main/stores.html', context=context)


@login_required(login_url='/login/')
@staff_only
def store(request):
    store = Store.objects.all()
    context = {
        'store':store,
    }
    return render(request, 'main/store.html', context=context)


@login_required(login_url='/login/')
@staff_only
def product_units(request, pk):
    product_model = get_object_or_404(ProductModel, id=pk)
    unitform = ProductUnitForm()
    if request.is_ajax():
        available_units = ProductUnit.objects.filter(product_model=product_model, status='Available')
        data = {
            'id': product_model.id,
            'name': product_model.name,
            'stock': product_model.units.count(),
            'price': product_model.price,
            'units': list(available_units.values()),
        }
        return JsonResponse(data)
    if request.method == 'POST':
        unitform = ProductUnitForm(request.POST)
        if unitform.is_valid():
            unit = unitform.save(commit=False)
            unit.product_model = product_model
            unit.save()
            return redirect('product_units', pk=pk)

    units = ProductUnit.objects.filter(product_model=product_model)
    products_filter = ProductUnitFilter(request.GET, queryset=units)
    units = products_filter.qs

    context = {
        'productmodel': product_model,
        'units': units,
        'unitform': unitform,
        'filter': products_filter,
    }
    return render(request, 'main/units.html', context=context)


@login_required(login_url='/login/')
def investor_dashboard(request):
    investor = get_object_or_404(Investor, user=request.user)
    products = investor.products.all()
    
    stock_price = 0
    for product in products:
        stock_price += product.product_model.purchase_price

    cash_in_hand = investor.balance - stock_price

    context = {
        'investor': investor,
        'products': products[:10],
        'stock_price': stock_price,
        'cash_in_hand': cash_in_hand,
    }
    return render(request, 'main/investor_dashboard.html', context)


@login_required(login_url='/login/')
def update_profile(request):
    form = UserForm(instance=request.user)
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'main/update_profile.html', context)


@login_required(login_url='/login/')
@admin_only
def managers(request):
    staffs = User.objects.filter(is_staff=True, is_superuser=False)

    context = {
        'staffs': staffs,
    }
    return render(request, 'main/managers.html', context)


@login_required(login_url='/login/')
@admin_only
def add_manager(request):
    form =  UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.is_staff = True
            staff.save()
            return redirect('managers')
    context = {
        'form': form,
    }
    return render(request, 'main/add_manager.html', context=context)


from django.views.generic.edit import View, UpdateView, DeleteView
from django.urls import reverse_lazy

class ProductDeleteView(DeleteView):
    model = ProductModel
    success_url = reverse_lazy('products')
    template_name = 'main/delete_template.html'


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')
    template_name = 'main/delete_template.html'


class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers')
    template_name = 'main/delete_template.html'


class InvestorDeleteView(DeleteView):
    model = Investor
    success_url = reverse_lazy('investors')
    template_name = 'main/delete_template.html'

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
    template_name = 'main/delete_template.html'


class StoreDeleteView(DeleteView):
    model = Store
    success_url = reverse_lazy('stores')
    template_name = 'main/delete_template.html'


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')
    template_name = 'main/delete_template.html'


class ProductUnitDeleteView(DeleteView):
    model = ProductUnit
    def get_success_url(self):
        product = self.object.product_model
        return reverse_lazy( 'product_units', kwargs={'pk': product.id})
    template_name = 'main/delete_template.html'


class ManagerDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('managers')
    template_name = 'main/delete_template.html'


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'phone', 'email', 'address']
    success_url = reverse_lazy('customers')
    template_name = 'main/update_template.html'
    

class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = '__all__'
    success_url = reverse_lazy('suppliers')
    template_name = 'main/update_template.html'


class InvestorUpdateView(UpdateView):
    model = Investor
    fields = ['phone', 'balance', 'profit']
    success_url = reverse_lazy('investors')
    template_name = 'main/update_template.html'


class ProductUpdateView(UpdateView):
    model = ProductModel
    form_class = ProductForm
    success_url = reverse_lazy('products')
    template_name = 'main/update_template.html'


@login_required(login_url='/login/')
@admin_only
def update_unit(request, pk):
    product = get_object_or_404(ProductUnit, id=pk)
    current_owner = product.owner
    form = ProductUnitUpdateForm(instance=product)


    if request.method == 'POST':
        form = ProductUnitUpdateForm(request.POST, instance=product)
        if form.is_valid():
            unit = form.save(commit=False)
            investor = unit.owner
            
            
            if investor and investor != current_owner:
                stock_price = 0
                for product in investor.products.all():
                    stock_price += product.product_model.purchase_price
                cash_in_hand = investor.balance - stock_price

                if cash_in_hand < unit.product_model.purchase_price:
                    form.add_error('owner', "Investor do not have sufficient balance to own this product.")
                    context = {
                        'form':form,
                    }
                    return render(request, 'main/update_template.html', context=context)

            unit.save()
            return redirect('product_units', pk=product.product_model.id)


    context = {
        'form': form,
    }
    return render(request, 'main/update_template.html', context=context)

class ManagerUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('managers')
    template_name = 'main/update_template.html'