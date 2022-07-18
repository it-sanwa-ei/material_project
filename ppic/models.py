from django.db import models

from django.utils import timezone


# Create your models here.
class ChangeOrder(models.Model):
    date_co = models.DateField(verbose_name='Tanggal', default=timezone.now)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    part_id_customer = models.CharField(verbose_name='Part No', max_length=255, blank=True, null=True)
    model = models.CharField(verbose_name='Model', max_length=255, blank=True, null=True)
    part_name = models.CharField(verbose_name='Nama Mold', max_length=255, blank=True, null=True)
    jumlah_produksi = models.PositiveIntegerField(verbose_name='Jumlah Produksi', blank=True, null=True)
    virgin = models.PositiveIntegerField(verbose_name='Usage Virgin', blank=True, null=True)
    regrind = models.PositiveIntegerField(verbose_name='Usage Regridn', blank=True, null=True)
    estimasi_selesai = models.DateField(verbose_name='Tanggal Selesai Produksi', blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    cycle_time = models.DecimalField(verbose_name='C/T', max_digits=6, decimal_places=2, default=0.00)
    cavity = models.PositiveIntegerField(verbose_name='Cavity', blank=True, null=True)
    output = models.PositiveIntegerField(verbose_name='Output', blank=True, null=True)
    no_mesin = models.CharField(verbose_name='M/C', max_length=255, blank=True, null=True)
    prioritas = models.PositiveIntegerField(verbose_name='Prioritas', blank=True, null=True)
    material_percentage = models.IntegerField(verbose_name='%', blank=True, null=True)