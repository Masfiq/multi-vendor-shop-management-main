import django_filters

from django_filters import CharFilter

from .models import *


class ProductUnitFilter(django_filters.FilterSet):
    serial = CharFilter(field_name='serial', label="Serial", lookup_expr='startswith')
    desc = CharFilter(field_name='short_description', label='Details', lookup_expr='icontains')
    class Meta:
        model = ProductUnit
        fields = ['serial', 'desc', 'store', 'supplier', 'status']


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', label='Product Title', lookup_expr='icontains')
    sku = CharFilter(field_name='sku', label='SKU starts', lookup_expr='startswith')

    class Meta:
        model = ProductModel
        fields = ['name', 'sku', 'categories']