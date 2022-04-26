from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from material.models import HopperFillData

from .views import ProductDeleteView, ProductDetailView, ProductListView, ProductCreateView, ProductUpdateView#, ProductSearchListView
from .views import HopperFillView, HopperDataListView
from .views import export_hopper_xls, export_hopper_xlsx

urlpatterns = [
    path('', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', staff_member_required(ProductCreateView.as_view()), name='product_input'),
    path('product/<int:pk>/edit/', staff_member_required(ProductUpdateView.as_view()), name='product_edit'),
    path('product/<int:pk>/delete', staff_member_required(ProductDeleteView.as_view()), name='product_delete'),
    path('product/hopper_fill/', login_required(HopperFillView.as_view()), name='hopper_fill'),
    path('product/hopper_fill_data/', HopperDataListView.as_view(), name='hopper_fill_data'),
    path('product/hopper_fill_data/export_hopper_xlsx/', export_hopper_xlsx, name='export_hopper_xlsx'),
    path('product/hopper_fill_data/export_hopper_xls/', export_hopper_xls, name='export_hopper_xls'),
]