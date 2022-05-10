from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import redirect

from material.models import HopperFillData

from .views import ProductDeleteView, ProductDetailView, ProductListView, ProductCreateView, ProductUpdateView#, ProductSearchListView
from .views import HopperFillView, HopperDataListView, HopperDataUpdateView, HopperDataDeleteView
from .views import export_hopper_xlsx, export_material_usage

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', staff_member_required(ProductCreateView.as_view(), login_url='login_admin'), name='product_input'),
    path('product/<int:pk>/edit/', staff_member_required(ProductUpdateView.as_view(), login_url='login_admin'), name='product_edit'),
    path('product/<int:pk>/delete', staff_member_required(ProductDeleteView.as_view(), login_url='login_admin'), name='product_delete'),
    path('product/hopper_fill/', login_required(HopperFillView.as_view(), login_url='login'), name='hopper_fill'),
    path('product/hopper_fill_data/', HopperDataListView.as_view(), name='hopper_fill_data'),
    path('product/hopper_fill_data/<int:pk>/edit/', login_required(HopperDataUpdateView.as_view(), login_url='login'), name='hopper_fill_edit'),
    path('product/hopper_fill_data/<int:pk>/delete/', staff_member_required(HopperDataDeleteView.as_view(), login_url='login_admin'), name='hopper_fill_delete'),
    path('product/hopper_fill_data/export_hopper_xlsx/', login_required(export_hopper_xlsx), name='export_hopper_xlsx'),
    path('product/hopper_fill_data/export_material_usage/', login_required(export_material_usage), name='export_material_usage'),
]