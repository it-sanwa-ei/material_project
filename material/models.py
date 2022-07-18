from django.conf import settings
from django.db import models
from django.urls import reverse

from datetime import datetime, date, time
import pytz

from material_project import settings
from django.contrib.auth import get_user_model as user_model

UserModel = user_model()

# Create your models here.

mesin_choice = []
for a in range(1, 35):
    mesin_choice.append(('A'+str(a), 'A'+str(a)))
for b in range(1, 24):
    mesin_choice.append(('B'+str(b), 'B'+str(b)))
for c in range(1, 44):
    mesin_choice.append(('C'+str(c), 'C'+str(c)))


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

class Product(models.Model):
    part_id = models.CharField('Part ID', max_length=20, blank=False, null=False)
    part_name = models.CharField('Part Name', max_length=100, blank=False, null=False)
    material = models.CharField('Material', max_length=100, blank=False, null=False)
    cycle_time = models.DecimalField('Cycle Time', max_digits=5, decimal_places=2, blank=False, null=False)
    customer = models.CharField('Customer', max_length=25, blank=False, null=False)
    part_weight = models.DecimalField('Part Weight', max_digits=6, decimal_places=3, blank=False, null=False)
    runner_weight = models.DecimalField('Runner Weight', max_digits=6, decimal_places=3, blank=False, null=False)
    cavity = models.PositiveIntegerField('Cavity', blank=False, null=False)

    def __str__(self):
        p = "{0.part_id} / {0.part_name} / {0.material}"
        return p.format(self)

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class HopperFillData(models.Model):
    no_mesin = models.CharField('No Mesin', max_length=3, choices=mesin_choice)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    no_lot = models.IntegerField('No Lot', blank=True, null=True)
    temp = models.IntegerField('Temperature', blank=False, null=False)
    tanggal = models.DateField('Tanggal', blank=False, null=False)
    jam_isi = models.TimeField('Jam Isi', blank=False, null=False)
    co_virgin = models.PositiveIntegerField('CO Virgin', blank=False, null=False, default=0)
    co_regrind = models.PositiveIntegerField('CO Regrind', blank=False, null=False, default=0)
    pemakaian_virgin = models.PositiveIntegerField('Usage Virgin', blank=False, null=False, default=0)
    pemakaian_regrind = models.PositiveIntegerField('Usage Regrind', blank=False, null=False, default=0)
    kebutuhan_material = models.IntegerField('Kebutuhan Material', blank=True, null=True)
    pic = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='PIC', to_field='username', blank=True, null=True)
    shift = models.CharField('Shift', max_length=7, blank=True, null=True)
    
    def __str__(self):
        hop = '{0.no_mesin}'
        return hop.format(self)
    
    def get_absolute_url(self):
        return reverse('hopper_fill_data')

    

class Scrap(models.Model):
    tanggal = models.DateField('Tanggal', blank=False, null=False)
    shift = models.CharField('Shift', max_length=7)
    jumlah_purge = models.DecimalField('Purging', decimal_places=2, max_digits=7)
    jumlah_ng = models.DecimalField('Part Scrap', decimal_places=2, max_digits=7)
    jumlah_runner = models.DecimalField('Runner', decimal_places=2, max_digits=7)
    pic = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='PIC', to_field='username', blank=True, null=True)

    def __str__(self):
        scrap = '{0.tanggal} / {0.shift}'
        return scrap.format(self)
    
    def get_absolute_url(self):
        return reverse('scrap_list')
    
class EstimasiMaterialUsageCO(models.Model):
    tanggal_co = models.DateField('Tanggal Co', blank=True, null=True)
    tanggal_operasi = models.DateField('Tanggal',blank=True, null=True)
    part_no = models.CharField('Part No', max_length=255, blank=True, null=True)
    target_output = models.PositiveIntegerField('Target Output', blank=True, null=True)
    total_berat_material = models.DecimalField('Total Berat Material', max_digits=200, decimal_places=2, blank=True, null=True)
    virgin_per_day = models.DecimalField('Virgin / Day', max_digits=200, decimal_places=2, blank=True, null=True)
    regrind_per_day = models.DecimalField('Regrind / Day', max_digits=200, decimal_places=2, blank=True, null=True)