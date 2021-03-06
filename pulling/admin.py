from django.contrib import admin

# Register your models here.

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin, ImportExportMixin

# Register your models here.

from .models import PullingFinishGoodItem, FinishGoodStock, ScanInModel, ScanOutModel

class PullingFinishGoodAdmin(admin.ModelAdmin):
    pass

class FinishGoodStockAdmin(ImportExportModelAdmin):
    pass

class ScanInAdmin(admin.ModelAdmin):
    pass

class ScanOutAdmin(admin.ModelAdmin):
    pass

admin.site.register(PullingFinishGoodItem, PullingFinishGoodAdmin)
admin.site.register(FinishGoodStock, FinishGoodStockAdmin)
admin.site.register(ScanInModel, ScanInAdmin)
admin.site.register(ScanOutModel, ScanOutAdmin)