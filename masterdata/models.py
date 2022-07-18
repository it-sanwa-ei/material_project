from django.db import models
from django.urls import reverse

# Create your models here.

class MasterDataCustomer(models.Model):
    code = models.CharField(verbose_name='Code', max_length=10, primary_key=True, blank=False, null=False)
    name = models.CharField(verbose_name='Customer', max_length=255, blank=False, null=False)
    address = models.CharField(verbose_name='Address', max_length=255, blank=True, null=False)
    city = models.CharField(verbose_name='City', max_length=25, blank=True, null=True)

    def __str__(self):
        cust = "{0.name}"
        return cust.format(self)

    def get_absolute_url(self):
        return reverse('md_customer_list')

class MasterDataProduct(models.Model):
    part_id_customer = models.CharField(verbose_name='Part ID Customer', max_length=50, blank=False, null=False)
    part_id_internal = models.CharField(verbose_name='Part ID Internal', max_length=25, primary_key=True)
    customer = models.ForeignKey(verbose_name='Customer', to=MasterDataCustomer,on_delete=models.CASCADE)
    part_name = models.CharField(verbose_name='Part Name', max_length=255, blank=False, null=False)
    material = models.CharField(verbose_name='Material', max_length=255, blank=False, null=False)
    
    def __str__(self):
        prod = "{0.part_id_customer}"
        return prod.format(self)
    
    def get_absolute_url(self):
        return reverse('md_product_list')
