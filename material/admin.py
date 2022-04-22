from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ExportMixin
from import_export.formats import base_formats

# Register your models here.
from .models import Product, HopperFillData
from .views import ImportProduct, ExportProduct
from .resources import ProductResources, HopperFillDataResources

class CustomAdminProduct(ImportExportMixin, admin.ModelAdmin):
    import_template_name = 'product_import.html'

    def get_import_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.CSV,
            base_formats.TSV,
        )
        return [f for f in formats if f().can_import()]

admin.site.register(Product, CustomAdminProduct)
admin.site.register(HopperFillData, admin.ModelAdmin)