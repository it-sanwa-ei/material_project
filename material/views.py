from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from regex import F

from tablib import Dataset
import csv
import xlwt
import xlsxwriter
import io

# Create your views here.
from .models import Product, HopperFillData
from .forms import HopperFillForm
from .resources import ProductResources, HopperFillDataResources

class HomeView(TemplateView):
    template_name = 'home.html'

class ProductListView(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'
    paginate_by = 50

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_input.html'
    fields = '__all__'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_edit.html'
    fields = '__all__'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product')



from datetime import datetime, date, time
import pytz

tz = pytz.timezone('Asia/Jakarta')
date_format = '%d/%m/%Y'
time_format = '%H:%M'
shift1_s = time(8, 0, 0)
shift1_e = time(15, 59, 59)
shift2_s = time(16, 0, 0)
shift2_e = time(23, 59, 59)
shift3_s = time(0, 0, 0)
shift3_e = time(7, 59, 59)
shift_choice = ['Shift 1', 'Shift 2', 'Shift 3']

class HopperFillView(LoginRequiredMixin, CreateView):
    form_class = HopperFillForm
    model = HopperFillData
    template_name = 'hopper_fill.html'
    success_url = reverse_lazy('home')

    
    def form_valid(self, form):
        no_mesin = form.cleaned_data['no_mesin']
        product = form.cleaned_data['product']
        no_lot = form.cleaned_data['no_lot']
        temp = form.cleaned_data['temp']
        tanggal = form.cleaned_data['tanggal']
        jumlah_isi = form.cleaned_data['jumlah_isi']
        jam_isi = form.cleaned_data['jam_isi']

        print(jam_isi)

        if (jam_isi >= shift1_s) and (jam_isi <= shift1_e):
            shift = shift_choice[0]
        elif (jam_isi >= shift2_s) and (jam_isi <= shift2_e):
            shift = shift_choice[1]
        elif (jam_isi >= shift3_s) and (jam_isi <= shift3_e):
            shift = shift_choice[2]

        temp = super(HopperFillView, self).form_valid(form = form)
        print(shift)
        form.instance.shift = shift
        form.instance.pic = self.request.user
        form.save()
        return temp

class HopperDataListView(ListView):
    model = HopperFillData
    template_name = 'hopper_fill_data.html'
    context_object_name = 'hopper_fill_data_list'
    paginate_by = 50

class ExportProduct(View):
    def __init__(self, request):
        self.request = request
        self.resource = ProductResources()
        self.dataset = self.resource.export().sort(col='id', reverse=True)

    def export_excel(self):
        response = HttpResponse(self.dataset.xls, content_type = 'application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename = "Part List.xls"'
        return response

    def export_csv(self):
        response = HttpResponse(self.dataset.csv, content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename = "Part List.csv"'
        return response

    def export_tsv(self):
        response = HttpResponse(self.dataset.tsv, content_type = 'text/tsv')
        response['Content-Disposition'] = 'attachment; filename = "Part List.tsv"'
        return response 

class ImportProduct(View):
    def __init__(self, request):
        self.request = request
        self.template = 'product_import.html'

    def simple_upload(self):
        if self.request.method == 'post':
            self.resource = ProductResources()
            self.dataset = Dataset()
            self.new_product_list = self.request.FILES['myfile']

            self.imported_data = self.dataset.load(self.new_product_list.read())
            self.result = self.resource.import_data(dataset=self.dataset, dry_run=True)

            if not self.result.has_errors():
                self.resource.import_data(dataset=self.dataset, dry_run=False)

        return render(request=self.request, template_name=self.template)

def export_hopper_xls(request):
    request = request

    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Hopper Fill Data ' + str(datetime.now().strftime('%d-%m-%Y')) + '.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Hopper Fill Data')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [ 'No Mesin', 'Part ID', 'Part Name',
                'Product Material', 'No Lot', 'Temperature', 'Tanggal', 
                'Jumlah Isi', 'Jam Isi', 'Shift', 'PIC']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = HopperFillData.objects.values_list('no_mesin', 'product__part_id', 'product__part_name',
                'product__material', 'no_lot', 'temp', 'tanggal', 
                'jumlah_isi', 'jam_isi', 'shift', 'pic').distinct()

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

def export_hopper_xlsx(request):
    request = request

    output = io.BytesIO()
    
    wb = xlsxwriter.Workbook(output, {'in_memory':True})
    ws = wb.add_worksheet(name = 'Hopper Fill Data')

    row_num = 0


    bold = wb.add_format({'bold':True})
    date_format = wb.add_format({'num_format':'d mmm yyyy'})
    time_format = wb.add_format({'num_format':'hh:mm'})

    columns = [ 'No Mesin', 'Part ID', 'Part Name',
                'Product Material', 'No Lot', 'Temperature', 'Tanggal', 
                'Jumlah Isi', 'Jam Isi', 'Shift', 'PIC']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], bold)

    
    no_mesin = HopperFillData.objects.values_list('no_mesin', flat=True)
    part_id = HopperFillData.objects.values_list('product__part_id', flat=True)
    part_name = HopperFillData.objects.values_list('product__part_name', flat=True)
    material = HopperFillData.objects.values_list('product__material', flat=True)
    no_lot = HopperFillData.objects.values_list('no_lot', flat=True)
    temp = HopperFillData.objects.values_list('temp', flat=True)
    tanggal = HopperFillData.objects.values_list('tanggal', flat=True)
    jumlah_isi = HopperFillData.objects.values_list('jumlah_isi', flat=True)
    jam_isi = HopperFillData.objects.values_list('jam_isi', flat=True)
    shift = HopperFillData.objects.values_list('shift', flat=True)
    pic = HopperFillData.objects.values_list('pic', flat=True)

    r = 1
    c = 0
    for d in no_mesin:
        ws.write_string(r, c, d)
        r+=1
    r = 1
    for d in part_id:
        ws.write_string(r, c+1, d)
        r+=1
    r = 1
    for d in part_name:
        ws.write_string(r, c+2, d)
        r+=1
    r = 1
    for d in material:
        ws.write_string(r, c+3, d)
        r+=1
    r = 1
    for d in no_lot:
        ws.write_string(r, c+4, str(d))
        r+=1
    r = 1
    for d in temp:
        ws.write_number(r, c+5, d)
        r+=1
    r = 1
    for d in tanggal:
        ws.write_datetime(r, c+6, d, date_format)
        r+=1
    r = 1
    for d in jumlah_isi:
        ws.write_number(r, c+7, d)
        r+=1
    r = 1
    for d in jam_isi:
        ws.write_datetime(r, c+8, d, time_format)
        r+=1
    r = 1
    for d in shift:
        ws.write_string(r, c+9, d)
        r+=1
    r = 1
    for d in pic:
        ws.write_string(r, c+10, d)
        r+=1

    wb.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type = 'pplication/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename = Hopper Fill Data ' + str(datetime.now().strftime('%d-%m-%Y')) + '.xlsx'

    return response

