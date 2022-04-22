from django import forms
from django.forms import ModelForm
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from material_project import settings

from datetime import datetime, date, time
import pytz

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
                    'part_id' : ('Part ID'),
                    'no_lot' : ('No Lot'),
                    'temp' : ('Temperature (°C)'),
                    'tanggal' : ('Tanggal'),
                    'jumlah_isi' : ('Jumlah Isi (kg)'),
                    'jam_isi' : ('Jam Isi'),
                    'pic' : ('PIC'), 
        }

        field_order = [ 'no_mesin', 'part_id', 'no_lot',
                        'temp', 'tanggal', 'jumlah_isi',
                        'jam_isi', 'pic', 'shift']

    #tanggal = forms.DateField(input_formats=settings.DATE_FORMAT, widget=forms.SelectDateWidget, initial=date.today().strftime('%d/%m/%Y'))
    #jam_isi = forms.TimeField(input_formats=settings.TIME_FORMAT, widget=forms.TimeInput, initial=datetime.today().strftime('%H:%M'))
    



