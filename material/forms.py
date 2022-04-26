from random import choices
from django import forms
from django.forms import ModelForm
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import Q

from material_project import settings

from datetime import datetime, date, time
import pytz

from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import HopperFillData, Product


class HopperFillForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HopperFillForm, self).__init__(*args, **kwargs)
        self.fields['tanggal'].widget = forms.SelectDateWidget(years = range(2000, date.today().year+3))
        self.fields['tanggal'].initial = datetime.today()
        self.fields['jam_isi'].widget = forms.TimeInput(attrs={'type':'time'})
        self.fields['jam_isi'].input_formats = settings.TIME_FORMAT
        self.fields['jam_isi'].initial = datetime.today().strftime('%H:%M')
        self.fields['shift'].widget = forms.HiddenInput()
        self.fields['shift'].initial = 'Shift 1'
        self.fields['pic'].widget = forms.HiddenInput()
        self.fields['pic'].initial = None
        
    class Meta:
        model = HopperFillData
        fields = '__all__'
        labels = {  'no_mesin' : ('No Mesin'),
                    'product' : ('Product'),
                    'no_lot' : ('No Lot'),
                    'temp' : ('Temperature (°C)'),
                    'tanggal' : ('Tanggal'),
                    'jumlah_isi' : ('Jumlah Isi (kg)'),
                    'jam_isi' : ('Jam Isi'),
                    'pic' : ('PIC'), 
        }

        field_order = [ 'no_mesin', 'product', 'no_lot',
                        'temp', 'tanggal', 'jumlah_isi',
                        'jam_isi', 'pic', 'shift']

   



