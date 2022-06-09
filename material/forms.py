from django import forms
from django.forms import ModelForm, SelectDateWidget
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField
from django.core.exceptions import ValidationError

from material_project import settings

from datetime import datetime, date, time
import pytz
tz = pytz.timezone('Asia/Jakarta')


from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import HopperFillData, Product, Scrap

class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('part_id', css_class = 'col-md-4'),
                Column('part_name', css_class = 'col-md-8'),
                css_class = 'row'
                ),
            Row(
                Column('material', css_class = 'col-md-10'),
                Column(AppendedText('cycle_time', 'sec'), css_class = 'col-md-2'),
                css_class = 'row'
                ),
            Row(
                Column('customer', css_class = 'col-md-6'),
                Column(AppendedText('part_weight', 'gr'), css_class = 'col-md-2'),
                Column(AppendedText('runner_weight', 'gr'), css_class = 'col-md-2'),
                Column('cavity', css_class = 'col-md-2'),
                css_class = 'row'
                ),
            Submit('submit_product', 'Save Product')
        )
    
    class Meta:
        model = Product
        fields = '__all__'

class HopperForm(ModelForm):
    total_co = forms.IntegerField(label='Total CO', required=False)
    def __init__(self, *args, **kwargs):
        super(HopperForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('no_mesin', css_class = 'col-md-2'),
                Column('product', css_class = 'col-md-7'),
                Column('no_lot', css_class = 'col-md-1'),
                Column(AppendedText('temp', '°C'), css_class = 'col-md-2'),
                css_class = 'row'
            ),
            Row(
                Column(MultiWidgetField('tanggal', attrs = ({'style':'width : 30%; display : inline-block; margin-right : 0.15em'})), css_class = 'col-md-8'),
                Column('jam_isi', css_class = 'col-md-4'),
                css_class = 'row'
            ),
            Row(
                Column(AppendedText('co_virgin', 'kg'), css_class = 'col-md-3'),
                Column(AppendedText('co_regrind', 'kg'), css_class = 'col-md-3'),
                Column(AppendedText('pemakaian_virgin', 'kg'), css_class = 'col-md-3'),
                Column(AppendedText('pemakaian_regrind', 'kg'), css_class = 'col-md-3'),
                css_class = 'row'
            ),
            Row(
                Column(AppendedText('total_co', 'kg'), css_class = 'col-md-6'),
                Column(AppendedText('kebutuhan_material', 'kg'), css_class = 'col-md-6'),
            ),
            Submit('submit_material_hopper', 'Submit Material Hopper')
        )

        self.fields['no_mesin'].initial = 'A1'
        self.fields['tanggal'].widget = SelectDateWidget(years= range(2000, datetime.today().year + 3))
        self.fields['tanggal'].initial = date.today()
        self.fields['jam_isi'].widget = forms.TimeInput(attrs={'type':'time'})
        self.fields['jam_isi'].initial = datetime.now().astimezone(tz=tz).strftime('%H:%M')
        self.fields['shift'].widget = forms.HiddenInput()
        self.fields['shift'].initial = 'Shift 1'
        self.fields['pic'].widget = forms.HiddenInput()
        self.fields['pic'].initial = None
        self.fields['total_co'].widget.attrs['readonly'] = True
        self.fields['total_co'].initial = 0
        self.fields['kebutuhan_material'].widget.attrs['readonly'] = True
        print(self.errors)
    
    class Meta:
        model = HopperFillData
        fields = '__all__'

class ScrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScrapForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                MultiWidgetField('tanggal', attrs = ({'style':'width : 32.5%; display: inline-block; margin-right:0.15em'},)),
                css_class = 'row'
                ),
            Row(
                Column('shift', css_class='col-md-4'), 
                css_class = 'row'),
            Row(
                Column(AppendedText('jumlah_purge', 'kg'), css_class='col-md-4'),
                Column(AppendedText('jumlah_ng', 'kg'), css_class='col-md-4'),
                Column(AppendedText('jumlah_runner', 'kg'), css_class='col-md-4'),
                css_class = 'row'
            ),
            Submit('submit_scrap', 'Submit Scrap')
        )

        self.fields['tanggal'].widget = SelectDateWidget(years = range(2000, date.today().year+3))
        self.fields['tanggal'].initial = datetime.today()
        shift_choices = (('Shift 1', 'Shift 1'), ('Shift 2', 'Shift 2'), ('Shift 3', 'Shift 3'),)
        self.fields['shift'] = forms.ChoiceField(choices=shift_choices)
        self.fields['shift'].initial = self.get_shift()
        self.fields['pic'].widget = forms.HiddenInput()
        self.fields['pic'].initial = None
        self.fields['jumlah_purge'].initial = 0.00
        self.fields['jumlah_ng'].initial = 0.00
        self.fields['jumlah_runner'].initial = 0.00

        
    def get_shift(self):
        tz = pytz.timezone('Asia/Jakarta')
        get_time_str = datetime.now(tz = tz).strftime('%H:%M')
        get_time_h = get_time_str[:2]
        get_time_m = get_time_str[3:5]

        get_time = time(int(get_time_h), int(get_time_m), 0)
        shift1_s = time(8, 0, 0)
        shift1_e = time(15, 59, 59)
        shift2_s = time(16, 0, 0)
        shift2_e = time(23, 59, 59)
        shift3_s = time(0, 0, 0)
        shift3_e = time(7, 59, 59)

        if get_time >= shift1_s and get_time <= shift1_e:
            return 'Shift 1'
        elif get_time >= shift2_s and get_time <= shift2_e:
            return 'Shift 2'
        else:
            return 'Shift 3'
    
    class Meta:
        model = Scrap
        fields = '__all__'
        labels = {  'tanggal' : ('Tanggal'),
                    'shift' : ('Shift'),
                    'jumlah_purge' : ('Purging'),
                    'jumlah_ng' : ('Part Scrap'),
                    'jumlah_runner' : ('Runner'),
        }
        field_order = ['tanggal', 'shift', 'jumlah_purge', 'jumlah_ng', 'jumlah_runner',]
