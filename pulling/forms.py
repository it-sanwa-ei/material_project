from django import forms
from django.forms import ModelForm, SelectDateWidget
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField, Reset, Button, Div, HTML
from django.template.defaultfilters import linebreaks_filter
from django.urls import reverse

from material_project import settings

from datetime import datetime, date, time
import pytz
tz = pytz.timezone('Asia/Jakarta')

from .models import PullingCustomer, PullingProduct, PullingLabel
from .models import TempPullingScanInModel, TempPullingScanOutModel


class PullingCustomerForm(ModelForm):
    address1 = forms.CharField(max_length=155, required=True)
    address2 = forms.CharField(max_length=100, required=False)
    def __init__(self, *args, **kwargs):
        super(PullingCustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('code', css_class = 'col-md-2'),
                Column('name', css_class = 'col-md-10'),
                css_class = 'row'
                ),
            Row(
                Column('address1', css_class = 'col-md-12'),
                css_class = 'row'
                ),
            Row(
                Column('address2', css_class = 'col-md-8'),
                Column('city', css_class = 'col-md-4'),
                css_class = 'row'
                ),
            Div(
                Div(Submit('submit', 'Save', css_class = 'btn-primary'), css_class = 'd-inline float-start'),
                Div(
                    Reset('reset', 'Reset', css_class = 'btn-warning'),
                    Button('cancel', 'Back', onclick='history.back()', css_class='btn-danger'),
                    css_class = 'd-inline float-end',   
                    ),
                ),
        )
        print(self.errors)
    class Meta:
        model = PullingCustomer
        fields = '__all__'
        exclude = ('address',)

class PullingProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PullingProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('part_id_sanwa', css_class = 'col-md-6'),
                Column('part_id_customer', css_class = 'col-md-6'),
                css_class = 'row'
                ),
            Row(
                Column('customer', css_class = 'col-md-12'),
                css_class = 'row'
                ),
            Row(
                Column('part_name', css_class = 'col-md-12'),
                css_class = 'row'
                ),
            Row(
                Column('material', css_class = 'col-md-12'),
                css_class = 'row'
                ),
            Row(
                Column('rack', css_class = 'col-md-6'),
                Column(AppendedText('bin_quantity', 'pcs'), css_class = 'col-md-6'),
                css_class = 'row'
                ),
            Row(
                Column(AppendedText('packaging_quantity', 'pcs'), css_class = 'col-md-6'),
                Column(AppendedText('full_bin_quantity', 'pcs'), css_class = 'col-md-6'),
                css_class = 'row'
                ),
            Div(
                Div(Submit('submit', 'Save', css_class = 'btn-primary'), css_class = 'd-inline float-start'),
                Div(
                    Reset('reset', 'Reset', onclick="window.location.reload();", css_class = 'btn-warning'),
                    Button('cancel', 'Back', onclick='history.back()', css_class='btn-danger'),
                    css_class = 'd-inline float-end',   
                    ),
                ),
        )
    class Meta:
        model = PullingProduct
        fields = '__all__'

class PullingLabelForm(ModelForm):
    shift_choice = (('Shift 1 Group A','1A'), ('Shift 1 Group B','1B'), ('Shift 1 Group C','1C'), ('Shift 1 Group D','1D'), 
                    ('Shift 2 Group A','2A'), ('Shift 2 Group B','2B'), ('Shift 2 Group C','2C'), ('Shift 2 Group D','2D'), 
                    ('Shift 3 Group A','3A'), ('Shift 3 Group B','3B'), ('Shift 3 Group C','3C'), ('Shift 3 Group D','3D'))
    mesin = ['A', 'B', 'C']
    line_choice = []
    for m in mesin:
        if m == 'A':
            for i in range(1, 35):
                line_choice.append(('Mesin '+ m +' No. ' + str(i), m+str(i)))
        if m == 'B':
            for i in range(1, 24):
                line_choice.append(('Mesin '+ m +' No. ' + str(i), m+str(i)))
        if m == 'C':
            for i in range(1, 44):
                line_choice.append(('Mesin '+ m +' No. ' + str(i), m+str(i)))

    tooling_choice =    (('#1','#1'),('#2','#2'),('#3','#3'),('#4','#4'),('#5','#5'),
                        ('#6','#6'),('#7','#7'),('#8','#8'),('#9','#9'),('#10','#10'),)

    customer_choice = PullingCustomer.objects.values_list('name','name')
    customer_choice = tuple(customer_choice)

    customer = forms.ChoiceField(choices=customer_choice, required=True)
    part_id_sanwa = forms.CharField(max_length=255, required=False)
    part_name = forms.CharField(max_length=255, required=False)
    rack = forms.CharField(max_length=255, required=False)
    material = forms.CharField(max_length=255, required=False)
    full_bin_quantity = forms.IntegerField(required=False)
    shift_group = forms.ChoiceField(choices=shift_choice, label='Shift - Group', required=True)
    line = forms.ChoiceField(choices=line_choice, label='Line', required=True)
    bin_quantity = forms.IntegerField(min_value=0)
    packaging_quantity = forms.IntegerField(min_value=0)
    tooling = forms.ChoiceField(choices=tooling_choice, required=False, label='#Tooling')
    remarks = forms.CharField(max_length=255, required=False, label='Remarks')

    def __init__(self, *args, **kwargs):
        super(PullingLabelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('pulling_label_pdf')
        self.helper.attrs = {'target':'_blank'}
        self.helper.layout = Layout(
            Row(
                Column('pulling_product', css_class = 'col-md-4'),
                Column('customer', css_class = 'col-md-6'),
                Column('date', css_class = 'col-md-2'),
                css_class = 'row'
                ),
            Row(
                Column('part_id_sanwa', css_class = 'col-md-3'),
                Column('part_name', css_class = 'col-md-6'),
                Column('tooling', css_class = 'col-md-3'),
                css_class = 'row'
                ),
            Row(
                Column('rack', css_class = 'col-md-3'),
                Column('material', css_class = 'col-md-6'),
                Column(AppendedText('full_bin_quantity', 'pcs'), css_class = 'col-md-3'),
                css_class = 'row'
                ),
            Row(
                Column('shift_group', css_class = 'col-md-3'),
                Column('line', css_class = 'col-md-3'),
                Column(AppendedText('bin_quantity', 'pcs'), css_class = 'col-md-2'),
                Column(AppendedText('packaging_quantity', 'pcs'), css_class = 'col-md-2'),
                Column('remarks', css_class = 'col-md-2'),
                css_class = 'row'
                ),
            Div(
                HTML('<button type="submit" name="submit" class="btn btn-danger col-md-4 me-4 validate"><i class="fa-solid fa-print"></i> Print</button>'),
                HTML('<button type="button" onclick="window.location.reload();" class="btn btn-warning col-md-4"><i class="fa-solid fa-rotate-left"></i> Reset</button>'),
                css_class = 'text-center'
                ),
            
        )
        self.fields['date'].widget = forms.DateInput()
        self.fields['date'].initial = datetime.now(tz=tz).date()
        self.fields['pulling_product'].label = 'Part ID Customer'
        self.fields['pulling_product'].widget.attrs.update({'autofocus':'autofocus'})
        self.fields['part_id_sanwa'].label = 'Part ID Sanwa'
        self.fields['part_id_sanwa'].widget.attrs['readonly'] = True
        self.fields['part_name'].label = 'Part Name'
        self.fields['part_name'].widget.attrs['readonly'] = True
        self.fields['full_bin_quantity'].label = 'Full Bin Quantity'
        self.fields['full_bin_quantity'].widget.attrs['readonly'] = True
        self.fields['rack'].widget.attrs['readonly'] = True
        self.fields['material'].widget.attrs['readonly'] = True
        self.fields['bin_quantity'].label = 'Total Quantity'
        self.fields['packaging_quantity'].label = 'Packaging Quantity'

    class Meta:
        model = PullingLabel
        fields = '__all__'

class PullingLabelScanInForm(forms.Form):
    qr_data = forms.CharField(label='Scan Label Barcode', required=True)
    def __init__(self, *args, **kwargs):
        super(PullingLabelScanInForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('pulling_label_in_decode')
        self.helper.layout = Layout(
            Row(
                Column('qr_data', css_class = 'col-md-11', ),
                HTML('<button class="btn col-md-1"><img src="https://i.ibb.co/w42nwD7/scan-in.png" alt="scan-in" style="border: 1px solid rgb(13, 110, 253);border-radius:15%;" height="60px" /></button>'),
                css_class = 'row'
            )
        )
        self.fields['qr_data'].widget.attrs.update({'autofocus':'autofocus'})

class PullingLabelScanOutForm(forms.Form):
    qr_data = forms.CharField(label='Scan Label Barcode', required=True)
    def __init__(self, *args, **kwargs):
        super(PullingLabelScanOutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('pulling_label_out_decode')
        self.helper.layout = Layout(
            Row(
                Column('qr_data', css_class = 'col-md-11', ),
                HTML('<button class="btn col-md-1"><img src="https://i.ibb.co/dMHbwB9/scan-out.png" alt="scan-in" style="border: 1px solid rgb(13, 110, 253);border-radius:15%;" height="60px" /></button>'),
                css_class = 'row'
            )
        )
        self.fields['qr_data'].widget.attrs.update({'autofocus':'autofocus'})

class TempScanInForm(ModelForm):
    line = forms.CharField(label='No Mc', widget=forms.TextInput())
    part_id_customer = forms.CharField(label='Part ID Customer')
    part_name = forms.CharField(label='Part Name')
    quantity = forms.IntegerField(label='Quantity')

    def __init__(self,  *args, **kwargs):
        super(TempScanInForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('line', css_class = 'col-md-2', ),
                Column('part_id_customer', css_class = 'col-md-4'),
                css_class = 'row'
            ),
            Row(
                Column('part_name', css_class = 'col-md-8', ),
                Column('quantity', css_class = 'col-md-3'),
                css_class = 'row'
            ),
            Submit('submit', 'Save')
        )
        self.fields['line'].widget = forms.TextInput()
        self.fields['line'].widget.attrs.update({'autofocus':'autofocus'})
        self.fields['part_id_customer'].widget.attrs['readonly'] = True
        self.fields['part_name'].widget.attrs['readonly'] = True
        self.fields['quantity'].widget.attrs['readonly'] = True
        print(self.errors)
    
    class Meta:
        model = TempPullingScanInModel
        fields = ['line', 'part_id_customer', 'part_name', 'quantity', ]

class TempScanOutForm(ModelForm):
    stock = forms.IntegerField(label='Warehouse Stock')
    def __init__(self,  *args, **kwargs):
        super(TempScanInForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class = 'col-md-8'),
                Column('part_id_customer', css_class = 'col-md-4'),
                css_class = 'row'
            ),
            Row(
                Column('part_name', css_class = 'col-md-8'),
                Column('requirement', css_class='col-md-2'),
                Column('quantity', css_class = 'col-md-2'),
                css_class = 'row'
            ),
            Row(
                Column('lot_no',css_class='col-md-4'),
                Column('no_of_bin', css_class='col-md-2'),
                css_class = 'row'
            ),
            Row(
                Column('spq', css_class = 'col-md-3'),
                Column('rack', css_class = 'col-md-3'),
                Column('stock', css_class = 'col-md-4'),
                css_class = 'row'
            ),
            Submit('submit', 'Save')
        )
        self.fields['part_id_customer'].widget.attrs['readonly'] = True
        self.fields['part_name'].widget.attrs['readonly'] = True
        self.fields['lot_no'].widget.attrs['readonly'] = True
        self.fields['spq'].widget.attrs['readonly'] = True
        self.fields['stock'].widget.attrs['readonly'] = True
        print(self.errors)
    
    class Meta:
        model = TempPullingScanOutModel
        fields = ['customer', 'part_id_customer', 'part_name', 'requirement', 'quantity', 'no_of_bin', 'lot_no', 'spq', 'rack', ]
