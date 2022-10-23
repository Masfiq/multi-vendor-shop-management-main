from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .decorators import admin_only

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('update-profile/',  views.update_profile, name='update_profile'),
    path('products/', views.products, name='products'),
    path('product/<int:pk>/', views.product, name='product'),
    path('new-product/', views.new_product, name='new_product'),
    path('customers/', views.customers, name='customers'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('new-customer/', views.new_customer, name='new_customer'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:pk>/', views.order, name='order'),
    path('new-order/', views.new_order, name='new_order'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('new-supplier/', views.new_supplier, name='new_supplier'),   
    path('categories/', views.categories, name='categories'),
    path('stores/', views.stores, name='stores'),
    path('store/<int:pk>/', views.store, name='store'),
    path('product-units/<int:pk>/', views.product_units, name='product_units'),

    # all delete views
    path('product/<int:pk>/delete/', login_required(admin_only(views.ProductDeleteView.as_view())), name='delete_product'),
    path('customer/<int:pk>/delete/', login_required(admin_only(views.CustomerDeleteView.as_view())), name='delete_customer'),
    path('category/<int:pk>/delete/', login_required(admin_only(views.CategoryDeleteView.as_view())), name='delete_category'),
    path('store/<int:pk>/delete/', login_required(admin_only(views.StoreDeleteView.as_view())), name='delete_store'),
    path('order/<int:pk>/delete/', login_required(admin_only(views.OrderDeleteView.as_view())), name='delete_order'),
    path('product-unit/<int:pk>/delete/', login_required(admin_only(views.ProductUnitDeleteView.as_view())), name='delete_unit'),
    path('supplier/<int:pk>/delete/', login_required(admin_only(views.SupplierDeleteView.as_view())), name='delete_supplier'),
    path('investor/<int:pk>/delete/', login_required(admin_only(views.InvestorDeleteView.as_view())), name='delete_investor'),

    # update views
    path('customer/<int:pk>/update/', login_required(admin_only(views.CustomerUpdateView.as_view())), name='update_customer'),
    path('supplier/<int:pk>/update/', login_required(admin_only(views.SupplierUpdateView.as_view())), name='update_supplier'),
    path('investor/<int:pk>/update/', login_required(admin_only(views.InvestorUpdateView.as_view())), name='update_investor'),
    path('product/<int:pk>/update/', login_required(admin_only(views.ProductUpdateView.as_view())), name='update_product'),
    path('product-unit/<int:pk>/update/', views.update_unit, name='update_unit'),
    
    # admin only
    path('investors/', views.investors, name='investors'),
    path('investor/<int:pk>/', views.investor, name='investor'),
    path('new-investor/', views.new_investor, name='new_investor'),
    path('managers/', views.managers, name='managers'),
    path('add_manager/', views.add_manager, name='add_manager'),
    path('manager/<int:pk>/update/', login_required(admin_only(views.ManagerUpdateView.as_view())), name='update_manager'),
    path('manager/<int:pk>/delete/', login_required(admin_only(views.ManagerDeleteView.as_view())), name='delete_manager'),
    path('update-profit-share/', views.update_profit_share, name='update_profit_share'),
    path('release-profit/', views.release_profit, name='release_profit'),
    # investor 
    path('investor-dashboard/',  views.investor_dashboard, name='investor_dashboard'),

]
