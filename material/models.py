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
    part_id = models.CharField('Part ID', max_length=20, blank=False, null=False, unique=True)
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
    no_mesin = models.CharField('No Mesin', max_length=3, choices=mesin_choice, default=mesin_choice[0])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', default=None)
    no_lot = models.IntegerField('No Lot', blank=True, null=True)
    temp = models.IntegerField('Temperature', blank=False, null=False)
    tanggal = models.DateField('Tanggal', blank=False, null=False)
    jumlah_isi = models.IntegerField('Jumlah Isi', blank=False, null=False)
    jam_isi = models.TimeField('Jam Isi', blank=False, null=False)
    pic = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='PIC', to_field='username', blank=True, null=True)
    shift = models.CharField('Shift', max_length=7)

    def __str__(self):
        return self.no_mesin



