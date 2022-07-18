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

from .models import MasterDataCustomer, MasterDataProduct

class MasterDataCustomerForm(ModelForm):
    address1 = forms.CharField(max_length=155, required=True)
    address2 = forms.CharField(max_length=100, required=False)
    def __init__(self, *args, **kwargs):
        super(MasterDataCustomerForm, self).__init__(*args, **kwargs)
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
    class Meta:
        model = MasterDataCustomer
        fields = '__all__'
        exclude = ('address',)

class MasterDataProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MasterDataProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('part_id_internal', css_class = 'col-md-6'),
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
        model = MasterDataProduct
        fields = '__all__'

