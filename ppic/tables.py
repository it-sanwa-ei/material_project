import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import format_html
import itertools

from .models import ChangeOrder

class ChangeOrderTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    estimasi_selesai = tables.DateColumn(format = 'd-m-Y')
    def __init__(self, *args, **kwargs):
        super(ChangeOrderTable, self).__init__(*args, **kwargs)
        self.columns['counter'].column.attrs = {'th':{'style':'text-align:center; padding-left:0;'}, 'td':{'style':'text-align:center; padding-left:0; width: 5%'}}
        self.columns['customer'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['part_id_customer'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['model'].column.attrs = {'td':{'style':'width:15%;'}}
        self.columns['part_name'].column.attrs = {'td':{'style':'width:15%;'}}
        self.columns['jumlah_produksi'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['virgin'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['regrind'].column.attrs = {'td':{'style':'width:7.5%;'}}
        self.columns['estimasi_selesai'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['material'].column.attrs = {'td':{'style':'width:25%;'}}
        self.columns['cycle_time'].column.attrs = {'td':{'style':'width:5%;'}}
        self.columns['cavity'].column.attrs = {'td':{'style':'width:5%;'}}
        self.columns['output'].column.attrs = {'td':{'style':'width:10%;'}}
        self.columns['no_mesin'].column.attrs = {'td':{'style':'width:5%;'}}
        self.columns['prioritas'].column.attrs = {'td':{'style':'width:2.5%;'}}
        self.columns['material_percentage'].column.attrs = {'td':{'style':'width:2.5%;'}}

    class Meta:
        model = ChangeOrder
        fields = ['counter','customer', 'part_id_customer', 'model', 'part_name', 'jumlah_produksi', 'virgin', 'regrind', 'estimasi_selesai','material','cycle_time','cavity','output','no_mesin', 'prioritas', 'material_percentage'   ]
        attrs = {"class": "co_list_table_style mb-4"}

    def render_counter(self):
        self.counter = getattr(self, 'counter', itertools.count(start= self.page.start_index()))
        return next(self.counter)
