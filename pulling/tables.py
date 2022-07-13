import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import format_html
import itertools

from .models import PullingProduct, PullingCustomer, PullingFinishGoodItem, FinishGoodStock
from .models import TempPullingScanInModel, TempPullingScanOutModel
from .models import ScanInModel, ScanOutModel

class PullingCustomerTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    edit = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('pulling_customer_edit',{"pk":tables.A('pk')}))
    delete = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('pulling_customer_delete',{"pk":tables.A('pk')}))
    def __init__(self, *args, **kwargs):
        super(PullingCustomerTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 5%'}}
        self.columns['code'].column.attrs = {'td':{'style':'width:5%;'}}
        self.columns['name'].column.attrs = {'td':{'style':'width:25%;'}}
        self.columns['address'].column.attrs = {'td':{'style':'width:45%;'}}
        self.columns['city'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['edit'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-warning', 'style':'width:5%'}}
        self.columns['delete'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-danger', 'style':'width:5%'}}

    class Meta:
        model = PullingCustomer
        fields = ['counter','code', 'name', 'address', 'city', 'edit', 'delete']
        attrs = {"class": "pulling_customer mb-4"}
    
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

class PullingProductTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    edit = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('pulling_product_edit',{"pk":tables.A('pk')}))
    delete = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('pulling_product_delete',{"pk":tables.A('pk')}))
    def __init__(self, *args, **kwargs):
        super(PullingProductTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0'}}
        self.columns['part_id_sanwa'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['material'].column.attrs = {'td':{'style':'width:25%;'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:17.5%;'}}
        self.columns['edit'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-warning', 'style':'width:5%'}}
        self.columns['delete'].column.attrs = {'th':{'style':'width:5%;'},'td':{'class':'text-center btn-danger', 'style':'width:5%'}}
    
    class Meta:
        model = PullingProduct
        fields = ('counter','part_id_sanwa', 'part_id_customer', 'part_name', 'material', 'customer', 'edit', 'delete',)
        attrs = {"class": "pulling_product mb-4"}

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


class PullingFinishGoodItemTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    date_time = tables.DateTimeColumn(format = 'd-m-Y / H:i')
    def __init__(self, *args, **kwargs):
        super(PullingFinishGoodItemTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 3%'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['lot_no'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['quantity'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['material'].column.attrs = {'td':{'style':'width:22.5%;'}}
        self.columns['ref_no'].column.attrs = {'td':{'style':'width:14.5%;'}}
        self.columns['date_time'].column.attrs = {'td':{'style':'width:7.5%;'}}
   
    class Meta:
        model = PullingFinishGoodItem
        fields = ['counter', 'part_id_customer', 'customer', 'lot_no', 'quantity', 'material', 'ref_no', 'date_time', ]
        attrs = {"class": "pulling_fg mb-4"}

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)

class TempScanInTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    line = tables.Column(empty_values=(), verbose_name='No Mc', orderable=True)
    date_time = tables.DateTimeColumn(format = 'd-m-Y / H:i')
    edit = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('temp_scan_in_edit',{"pk":tables.A('pk')}))
    delete = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('temp_scan_in_delete',{"pk":tables.A('pk')}))
    def __init__(self, *args, **kwargs):
        super(TempScanInTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 3%'}}
        self.columns['line'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['quantity'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['date_time'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['edit'].column.attrs = {'td':{'style':'width:3%; text-align:center;'}}
        self.columns['delete'].column.attrs = {'td':{'style':'width:3%; text-align:center;'}}
   
    class Meta:
        model = TempPullingScanInModel
        fields = ['counter', 'line', 'part_id_customer', 'customer', 'part_name', 'quantity', 'date_time', 'edit', 'delete']
        attrs = {"class": "pulling_fg mb-4"}
    
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

class TempScanOutTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    date_time = tables.DateTimeColumn(format = 'd-m-Y / H:i')
    delete = tables.Column(empty_values=[], verbose_name='', orderable=False, linkify=('temp_scan_out_delete',{"pk":tables.A('pk')}))
    def __init__(self, *args, **kwargs):
        super(TempScanOutTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 3%'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['lot_no'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['quantity'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['rack'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['date_time'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['delete'].column.attrs = {'td':{'style':'width:3%; text-align:center;'}}
   
    class Meta:
        model = TempPullingScanOutModel
        fields = ['counter', 'customer', 'part_id_customer', 'part_name', 'quantity', 'lot_no', 'rack', 'date_time', 'delete']
        attrs = {"class": "pulling_fg mb-4"}

    
    def render_delete(self):
        if not self.columns['delete'].column.value():
            return format_html('<i class="fa-solid fa-trash-can"></i>')
        return self.columns['delete'].column.value()

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)


class FinishGoodStockTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    def __init__(self, *args, **kwargs):
        super(FinishGoodStockTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 3%'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:15%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:15%;'}}
        self.columns['material'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['total_quantity'].column.attrs = {'td':{'style':'width:7.5%;'}}
   
    class Meta:
        model = FinishGoodStock
        fields = ['counter', 'customer', 'part_id_customer', 'part_name', 'material', 'total_quantity', ]
        attrs = {"class": "pulling_product mb-4"}

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)

class ScanInTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    date_time = tables.DateTimeColumn(format = 'd-m-Y / H:i')
    def __init__(self, *args, **kwargs):
        super(ScanInTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 3%'}}
        self.columns['line'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['lot_no'].column.attrs = {'td':{'style':'width:8.5%;'}}
        self.columns['quantity'].column.attrs = {'td':{'style':'width:6.5%;'}}
        self.columns['rack'].column.attrs = {'td':{'style':'width:8.5%;'}}
        self.columns['date_time'].column.attrs = {'td':{'style':'width:8%;'}}
   
    class Meta:
        model = ScanInModel
        fields = ['counter', 'line', 'part_id_customer', 'part_name', 'customer', 'lot_no', 'quantity', 'rack', 'date_time']
        attrs = {"class": "pulling_fg mb-4"}

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)

class ScanOutTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    date_time = tables.DateTimeColumn(format = 'd-m-Y / H:i')
    def __init__(self, *args, **kwargs):
        super(ScanOutTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 3%'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:12.5%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:20%;'}}
        self.columns['lot_no'].column.attrs = {'td':{'style':'width:8.5%;'}}
        self.columns['quantity'].column.attrs = {'td':{'style':'width:6.5%;'}}
        self.columns['spq'].column.attrs = {'td':{'style':'width:6.5%;'}}
        self.columns['rack'].column.attrs = {'td':{'style':'width:8.5%;'}}
        self.columns['date_time'].column.attrs = {'td':{'style':'width:8%;'}}
   
    class Meta:
        model = ScanOutModel
        fields = ['counter','customer', 'part_id_customer', 'part_name', 'lot_no', 'quantity', 'spq', 'rack', 'date_time']
        attrs = {"class": "pulling_fg mb-4"}

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)