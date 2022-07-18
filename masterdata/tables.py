import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import format_html
import itertools

from .models import MasterDataCustomer, MasterDataProduct

class MasterDataCustomerTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    edit = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('md_customer_edit',{"pk":tables.A('code')}))
    delete = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('md_customer_delete',{"pk":tables.A('code')}))
    def __init__(self, *args, **kwargs):
        super(MasterDataCustomerTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 5%'}}
        self.columns['code'].column.attrs = {'th':{'style':'width:5%;'}, 'td':{'style':'width:5%;'}}
        self.columns['name'].column.attrs = {'th':{'style':'width:25%;'}, 'td':{'style':'width:25%;'}}
        self.columns['address'].column.attrs = {'th':{'style':'width:45%;'}, 'td':{'style':'width:45%;'}}
        self.columns['city'].column.attrs = {'th':{'style':'width:10%;'}, 'td':{'style':'width:10%;'}}
        self.columns['edit'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-warning', 'style':'width:5%'}}
        self.columns['delete'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-danger', 'style':'width:5%'}}

    class Meta:
        model = MasterDataCustomer
        fields = ['counter','code', 'name', 'address', 'city', 'edit', 'delete']
        attrs = {"class": "md_customer mb-4"}
    
    def render_edit(self):
        if not self.columns['edit'].column.value():
            return format_html('<i class="fa-solid fa-pen"></i>')
        return self.columns['edit'].column.value()
    
    def render_delete(self):
        if not self.columns['delete'].column.value():
            return format_html('<i class="fa-solid fa-trash-can"></i>')
        return self.columns['delete'].column.value()

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)

class MasterDataProductTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    edit = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('md_product_edit',{"pk":tables.A('pk')}))
    delete = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('md_product_delete',{"pk":tables.A('pk')}))
    def __init__(self, *args, **kwargs):
        super(MasterDataProductTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0'}}
        self.columns['part_id_internal'].column.attrs = {'th':{'style':'width:10%;'}, 'td':{'style':'width:10%;'}}
        self.columns['part_id_customer'].column.attrs = {'th':{'style':'width:12.5%;'}, 'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'th':{'style':'width:20%;'},'td':{'style':'width:20%;'}}
        self.columns['material'].column.attrs = {'th':{'style':'width:25%;'}, 'td':{'style':'width:25%;'}}
        self.columns['customer'].column.attrs = {'th':{'style':'width:17.5%;'}, 'td':{'style':'width:17.5%;'}}
        self.columns['edit'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-warning', 'style':'width:5%'}}
        self.columns['delete'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-danger', 'style':'width:5%'}}
    
    class Meta:
        model = MasterDataProduct
        fields = ('counter','part_id_internal', 'part_id_customer', 'part_name', 'material', 'customer', 'edit', 'delete',)
        attrs = {"class": "md_product mb-4"}

    def render_edit(self):
        if not self.columns['edit'].column.value():
            return format_html('<i class="fa-solid fa-pen"></i>')
        return self.columns['edit'].column.value()
    
    def render_delete(self):
        if not self.columns['delete'].column.value():
            return format_html('<i class="fa-solid fa-trash-can"></i>')
        return self.columns['delete'].column.value()

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)
