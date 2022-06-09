from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import redirect

from .views import ProductDeleteView, ProductDetailView, ProductListView, ProductCreateView, ProductUpdateView
from .views import HopperCreateView, HopperListView, HopperUpdateView, HopperDeleteView
from .views import ScrapCreateView, ScrapListView, ScrapUpdateView, ScrapDeleteView
from .views import export_hopper_xlsx, export_material_usage, ajax_fill_hopper_form, import_product_xlsx, export_scrap_xlsx

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', staff_member_required(ProductCreateView.as_view(), login_url='login_admin'), name='product_input'),
    path('product/<int:pk>/edit/', staff_member_required(ProductUpdateView.as_view(), login_url='login_admin'), name='product_edit'),
    path('product/<int:pk>/delete', staff_member_required(ProductDeleteView.as_view(), login_url='login_admin'), name='product_delete'),
    path('product/import_xlsx/', staff_member_required(import_product_xlsx, login_url='login_admin'), name='import_product_xlsx'),
    path('hopper_fill/new/', login_required(HopperCreateView.as_view(), login_url='login'), name='hopper_fill'),
    path('hopper_fill_list/', login_required(HopperListView.as_view(), login_url='login'), name='hopper_fill_data'),
    path('hopper_fill_list/<int:pk>/edit/', login_required(HopperUpdateView.as_view(), login_url='login'), name='hopper_fill_edit'),
    path('hopper_fill_list/<int:pk>/delete/', login_required(HopperDeleteView.as_view(), login_url='login'), name='hopper_fill_delete'),
    path('hopper_fill_list/export_hopper_xlsx/', login_required(export_hopper_xlsx, login_url='login'), name='export_hopper_xlsx'),
    path('hopper_fill_list/export_material_usage/', login_required(export_material_usage, login_url='login'), name='export_material_usage'),
    path('hopper_fill/ajax/hopper/', ajax_fill_hopper_form, name='ajax_fill_hopper_form'),
    path('scrap_form/new/', login_required(ScrapCreateView.as_view(), login_url='login'), name='scrap_input'),
    path('scrap_list/', login_required(ScrapListView.as_view(), login_url='login'), name='scrap_list'),
    path('scrap_list/<int:pk>/edit/', login_required(ScrapUpdateView.as_view(), login_url='login'), name='scrap_edit'),
    path('scrap_list/<int:pk>/delete/', login_required(ScrapDeleteView.as_view(), login_url='login'), name='scrap_delete'),
    path('scrap_list/export_scrap_xlsx/', login_required(export_scrap_xlsx, login_url='login'), name='export_scrap_xlsx'),
]