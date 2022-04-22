from import_export import resources

from .models import Product, HopperFillData

class ProductResources(resources.ModelResource):
    class Meta:
        model = Product
        fields = '__all__'

class HopperFillDataResources(resources.ModelResource):
    class Meta:
        model = HopperFillData
        fields = '__all__'
        clean_model_instances = True
        widgets = {
            'tanggal' : {'format':'%d-%m-%Y'}
        }
        export_order = ('no_mesin', 'product__part_id', 'product__part_name',
                        'product__material', 'no_lot', 'temp', 'tanggal', 
                        'jumlah_isi', 'jam_isi', 'shift', 'pic')