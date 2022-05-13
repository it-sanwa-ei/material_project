from email import message
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.list import BaseListView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.core import signing
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core.signing import BadSignature
from django.core.cache import cache

from datetime import datetime, date, time, timedelta

from tablib import Dataset
import csv
import xlwt
import xlsxwriter
import io

# Create your views here.
from .models import Product, HopperFillData
from .forms import HopperFillForm
from .resources import ProductResources, HopperFillDataResources
from material_project import settings

class HomeView(TemplateView):
    template_name = 'home.html'

class ProductListView(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter( Q(part_id__icontains=query) | Q(part_name__icontains=query) | Q(material__icontains=query))
        else:
            return Product.objects.all().order_by('id')
    
    
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
    success_url = "/"
    paginate_by = 50

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
    ordering = ['-id']

class HopperDataUpdateView(UpdateView):
    model = HopperFillData
    template_name = 'hopper_fill_edit.html'
    fields = ('no_mesin','product','no_lot','temp','tanggal','jumlah_isi','jam_isi')

class HopperDataDeleteView(DeleteView):
    model = HopperFillData
    template_name = 'hopper_fill_delete.html'
    context_object_name = 'hopper_delete'
    success_url = reverse_lazy('hopper_fill_data')

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


def export_hopper_xlsx(request):
    if request.method == 'POST':
        if request.POST.get('request_date_start'):
            request_date_start = request.POST.get('request_date_start')
            request_date_start = datetime.strptime(request_date_start, '%Y-%m-%d')
        else:
            request_date_start = datetime.strptime(datetime.now(tz=tz).strftime('%Y-%m-%d'), '%Y-%m-%d')

        if request.POST.get('request_date_end'):
            request_date_end = request.POST.get('request_date_end')
            request_date_end = datetime.strptime(request_date_end, '%Y-%m-%d')
        else:
            request_date_end = datetime.strptime(datetime.now(tz=tz).strftime('%Y-%m-%d'), '%Y-%m-%d')
    else:
        pass


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

    
    filtered_query = HopperFillData.objects.filter(tanggal__gte=request_date_start.date(), tanggal__lte=request_date_end.date())

    if filtered_query:
        no_mesin = filtered_query.values_list('no_mesin', flat=True).order_by('tanggal', 'jam_isi')
        part_id = filtered_query.values_list('product__part_id', flat=True).order_by('tanggal', 'jam_isi')
        part_name = filtered_query.values_list('product__part_name', flat=True).order_by('tanggal', 'jam_isi')
        material = filtered_query.values_list('product__material', flat=True).order_by('tanggal', 'jam_isi')
        no_lot = filtered_query.values_list('no_lot', flat=True).order_by('tanggal', 'jam_isi')
        temp = filtered_query.values_list('temp', flat=True).order_by('tanggal', 'jam_isi')
        tanggal = filtered_query.values_list('tanggal', flat=True).order_by('tanggal', 'jam_isi')
        jumlah_isi = filtered_query.values_list('jumlah_isi', flat=True).order_by('tanggal', 'jam_isi')
        jam_isi = filtered_query.values_list('jam_isi', flat=True).order_by('tanggal', 'jam_isi')
        shift = filtered_query.values_list('shift', flat=True).order_by('tanggal', 'jam_isi')
        pic = filtered_query.values_list('pic', flat=True).order_by('tanggal', 'jam_isi')

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

        response = HttpResponse(output.read(), content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename = Hopper Fill Data ' + str(request_date_start.strftime('%d-%m-%Y')) + '_-_' +  str(request_date_end.strftime('%d-%m-%Y')) + '.xlsx'

        
    else:
        wb.close()
        output.seek(0)

        url = reverse_lazy('hopper_fill_data')
        warning = '0 Entry with date between ' + str(request_date_start.date()) + ' and ' + str(request_date_end.date())

        response = HttpResponse("<script> alert( '%s' ); window.location='%s' </script>" %(warning, url))

    return response
    

def get_material_used_per_day(no_mesin, part_id, part_name, material, no_lot, temp, tanggal, jumlah_isi, jam_isi, shift, pic):
    no_mesin = no_mesin.order_by('-tanggal')
    part_id = part_id.order_by('-tanggal')
    part_name = part_name.order_by('-tanggal')
    material = material.order_by('-tanggal')
    no_lot = no_lot.order_by('-tanggal')
    temp = temp.order_by('-tanggal')
    tanggal = tanggal.order_by('-tanggal')
    jumlah_isi = jumlah_isi.order_by('-tanggal')
    jam_isi = jam_isi.order_by('-tanggal')
    shift = shift.order_by('-tanggal')
    pic = pic.order_by('-tanggal')

    temp_qs = []

    for i in range(0, len(no_mesin)):
        q = [no_mesin[i], part_id[i], part_name[i], material[i], no_lot[i], temp[i], tanggal[i],
         jumlah_isi[i], jam_isi[i], shift[i], pic[i]]
        temp_qs.append(q)

    gr_start_id = []
    gr_start_id.append(0)

    gr = 1

    for i in range(0, len(temp_qs)):
        try:
            if temp_qs[i][6] != temp_qs[i+1][6]:
                gr += 1
                gr_start_id.append(i+1)
            else:
                pass
        except IndexError:
            pass
    
    def gr_per_date(gr_t, gr_st_id):
        gr_qs = []
        for g in range(0, len(gr_st_id)-1):
            gr_qs.append(gr_t[gr_st_id[g]:gr_st_id[g+1]])
        gr_qs.append(gr_t[gr_st_id[-1]:len(gr_t)])
        return gr_qs

    gr_qs = gr_per_date(temp_qs, gr_start_id)

    def gr_per_mat(gr_qs):
        mat = []
        result = []
        for qs in gr_qs:
            for q in qs:
                if q[3] not in mat:
                    mat.append(q[3])

            for m in mat:
                amount = 0
                for q in qs:
                    if q[3] == m:
                        amount += q[7]
                result.append([qs[0][6], m, amount])
        return result

    result = gr_per_mat(gr_qs) 
    return result

def export_material_usage(request):
    if request.method == 'POST':
        request_date = request.POST.get('request_date')
        if request_date:
            request_date = datetime.strptime(request_date, '%Y-%m-%d')
        else:
            request_date = datetime.strptime(datetime.now(tz=tz).strftime('%Y-%m-%d'), '%Y-%m-%d')
    else:
        pass

    print(request_date)

    output = io.BytesIO()
    
    wb = xlsxwriter.Workbook(output, {'in_memory':True})
    ws_1 = wb.add_worksheet(name = 'Material Usage Report - Daily')
    ws_2 = wb.add_worksheet(name = 'Material Usage Report - Weekly')
    ws_3 = wb.add_worksheet(name = 'Material Usage Report - Monthly')

    bold = wb.add_format({'bold':True})
    date_format = wb.add_format({'num_format':'d mmm yyyy'})
    
    no_mesin = HopperFillData.objects.values_list('no_mesin', flat=True).order_by('-id')
    part_id = HopperFillData.objects.values_list('product__part_id', flat=True).order_by('-id')
    part_name = HopperFillData.objects.values_list('product__part_name', flat=True).order_by('-id')
    material = HopperFillData.objects.values_list('product__material', flat=True).order_by('-id')
    no_lot = HopperFillData.objects.values_list('no_lot', flat=True).order_by('-id')
    temp = HopperFillData.objects.values_list('temp', flat=True).order_by('-id')
    tanggal = HopperFillData.objects.values_list('tanggal', flat=True).order_by('-id')
    jumlah_isi = HopperFillData.objects.values_list('jumlah_isi', flat=True).order_by('-id')
    jam_isi = HopperFillData.objects.values_list('jam_isi', flat=True).order_by('-id')
    shift = HopperFillData.objects.values_list('shift', flat=True).order_by('-id')
    pic = HopperFillData.objects.values_list('pic', flat=True).order_by('-id')

    daily_material_usage = get_material_used_per_day(no_mesin=no_mesin, part_id=part_id, part_name=part_name,
                            material=material, no_lot=no_lot, temp=temp, tanggal=tanggal, jumlah_isi=jumlah_isi,
                            jam_isi=jam_isi, shift=shift, pic=pic)

    x, y = 1, 0
    ws_1.write(0, 0, 'Tanggal', bold)
    ws_1.write(0, 1, 'Material', bold)
    ws_1.write(0, 2, 'Jumlah yang digunakan (kg)', bold)

    #untuk ws_1 (daily)
    for dl in daily_material_usage:
        if dl[2] != 0:
            if dl[0] == request_date.date():
                ws_1.write_datetime(x, y, dl[0], date_format)
                ws_1.write_string(x, y+1, dl[1])
                ws_1.write_number(x, y+2, dl[2])
                x += 1
            else:
                pass
        else:
            pass
    pass

    x, y = 1, 0
    ws_2.write(0, 0, 'Tanggal', bold)
    ws_2.write(0, 1, 'Material', bold)
    ws_2.write(0, 2, 'Jumlah yang digunakan (kg)', bold)

    #untuk ws_2 (weekly)
    date_start = request_date.date()
    date_end = request_date.date() - timedelta(days=7)
    for dl in daily_material_usage:
        if dl[2] != 0:
            if dl[0] <= date_start and dl[0] >= date_end:
                ws_2.write_datetime(x, y, dl[0], date_format)
                ws_2.write_string(x, y+1, dl[1])
                ws_2.write_number(x, y+2, dl[2])
                x += 1
            else:
                pass
        else:
            pass
    pass

    x, y = 1, 0
    ws_3.write(0, 0, 'Tanggal', bold)
    ws_3.write(0, 1, 'Material', bold)
    ws_3.write(0, 2, 'Jumlah yang digunakan (kg)', bold)

    #untuk ws_3 (monthly)
    date_start = request_date.date()
    date_end = request_date.date() - timedelta(days=30)
    for dl in daily_material_usage:
        if dl[2] != 0:
            if dl[0] <= date_start and dl[0] >= date_end:
                ws_3.write_datetime(x, y, dl[0], date_format)
                ws_3.write_string(x, y+1, dl[1])
                ws_3.write_number(x, y+2, dl[2])
                x += 1
            else:
                pass
        else:
            pass
    pass

    wb.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename = Material Usage Report ' + str(request_date.strftime('%d-%m-%Y')) + '.xlsx'

    return response
    