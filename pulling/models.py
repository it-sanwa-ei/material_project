from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models import Sum

# Create your models here.

class PullingCustomer(models.Model):
    code = models.CharField(verbose_name='Code', max_length=10, blank=False, null=False)
    name = models.CharField(verbose_name='Customer', max_length=255, blank=False, null=False)
    address = models.CharField(verbose_name='Address', max_length=255, blank=True, null=False)
    city = models.CharField(verbose_name='City', max_length=25, blank=True, null=True)

    def __str__(self):
        cust = "{0.name}"
        return cust.format(self)

    def get_absolute_url(self):
        return reverse('pulling_customer_list')

class PullingProduct(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=20, blank=False, null=False)
    part_id_sanwa = models.CharField(verbose_name='Part ID Internal', max_length=20, primary_key=True)
    customer = models.ForeignKey(verbose_name='Customer', to=PullingCustomer,on_delete=models.CASCADE)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=False, null=False)
    material = models.CharField(verbose_name='Material', max_length=255, blank=False, null=False)
    rack = models.CharField(verbose_name='Rack', max_length=20, blank=True, null=True)
    bin_quantity = models.PositiveIntegerField(verbose_name='Bin Quantity', blank=True, null=True)
    packaging_quantity = models.PositiveIntegerField(verbose_name='Packaging Quantity', blank=True, null=True)
    full_bin_quantity = models.PositiveIntegerField(verbose_name='Full Bin Quantity', blank=True, null=True)
    
    def __str__(self):
        prod = "{0.part_id_customer}"
        return prod.format(self)

    def get_absolute_url(self):
        return reverse('pulling_product_list')

class PullingLabel(models.Model):
    pulling_product = models.ForeignKey(to=PullingProduct, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Production Date')

    def __str__(self):
        label= "{0.product} / {0.date}"
        return label.format(self)
    
    def get_absolute_url(self):
        return reverse('pulling_label_pdf')


class PullingFinishGoodItem(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=255, blank=True, null=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=True, null=True)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    lot_no = models.CharField(verbose_name='Lot No.', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity', blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    ref_no = models.CharField(verbose_name='Ref No.', max_length=255, blank=True, null=True)
    note = models.TextField(verbose_name='Note', blank=True, null=True)
    date_time = models.DateTimeField(verbose_name='Date / Time', blank=True, null=True)

    def __str__(self):
        pfg = "{0.date_time} / {0.part_id_customer}"
        return pfg.format(self)

    def get_absolute_url(self):
        return reverse('pulling_finish_good_item_list')

class TempPullingScanInModel(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=255, blank=True, null=True)
    line = models.CharField(verbose_name='No Mc', max_length=255, blank=True, null=True)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=True, null=True)
    lot_no = models.CharField(verbose_name='Lot No.', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity', blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    ref_no = models.CharField(verbose_name='Ref No.', max_length=255, blank=True, null=True)
    note = models.TextField(verbose_name='Note', blank=True, null=True)
    date_time = models.DateTimeField(verbose_name='Date/Time', blank=True, null=True)
    pic = models.CharField(verbose_name='PIC', max_length=255, blank=True, null=True)

class ScanInModel(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=255, blank=True, null=True)
    line = models.CharField(verbose_name='No Mc', max_length=255, blank=True, null=True)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=True, null=True)
    lot_no = models.CharField(verbose_name='Lot No.', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity', blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    ref_no = models.CharField(verbose_name='Ref No.', max_length=255, blank=True, null=True)
    rack = models.CharField(verbose_name='Address', max_length=255, blank=True, null=True)
    note = models.TextField(verbose_name='Note', blank=True, null=True)
    date_time = models.DateTimeField(verbose_name='Date/Time', blank=True, null=True)
    pic = models.CharField(verbose_name='PIC', max_length=255, blank=True, null=True)

    def __str__(self):
        psi = "{0.date_time} / {0.part_id_customer}"
        return psi.format(self)

class TempPullingScanOutModel(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=255, blank=True, null=True)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=True, null=True)
    lot_no = models.CharField(verbose_name='Lot No.', max_length=255, blank=True, null=True)
    requirement = models.CharField(verbose_name='Requirement', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity', blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    no_of_bin = models.IntegerField(verbose_name='No of bin', blank=True, null=True)
    spq = models.CharField(verbose_name='SPQ', max_length=255, blank=True, null=True)
    rack = models.CharField(verbose_name='Rack', max_length=255, blank=True, null=True)
    note = models.TextField(verbose_name='Note', blank=True, null=True)
    date_time = models.DateTimeField(verbose_name='Date/Time', blank=True, null=True)
    pic = models.CharField(verbose_name='PIC', max_length=255, blank=True, null=True)

class ScanOutModel(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=255, blank=True, null=True)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=True, null=True)
    lot_no = models.CharField(verbose_name='Lot No.', max_length=255, blank=True, null=True)
    requirement = models.CharField(verbose_name='Requirement', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity', blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    no_of_bin = models.IntegerField(verbose_name='No of bin', blank=True, null=True)
    spq = models.CharField(verbose_name='SPQ', max_length=255, blank=True, null=True)
    rack = models.CharField(verbose_name='Address', max_length=255, blank=True, null=True)
    note = models.TextField(verbose_name='Note', blank=True, null=True)
    date_time = models.DateTimeField(verbose_name='Date/Time', blank=True, null=True)
    pic = models.CharField(verbose_name='PIC', max_length=255, blank=True, null=True)

    def __str__(self):
        pso = "{0.date_time} / {0.part_id_customer}"
        return pso.format(self)


class FinishGoodStock(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length= 255, primary_key=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=True, null=True)
    customer = models.CharField(verbose_name='Customer', max_length=255, blank=True, null=True)
    material = models.CharField(verbose_name='Material', max_length=255, blank=True, null=True)
    total_quantity = models.IntegerField(verbose_name='Total Quantity', blank=True, null=False, default=0)

    def __str__(self):
        fg = "{0.part_id_customer} / {0.part_name} / {0.customer} / {0.total_quantity} "
        return fg.format(self)

    def get_absolute_url(self):
        return reverse('finish_good_stock')