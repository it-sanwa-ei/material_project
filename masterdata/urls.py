from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .views import MasterDataHomeView
from .views import MasterDataCustomerCreateView, MasterDataCustomerListView, MasterDataCustomerUpdateView, MasterDataCustomerDeleteView, import_md_customer_xlsx
from .views import MasterDataProductCreateView, MasterDataProductListView, MasterDataProductUpdateView, MasterDataProductDeleteView, import_md_product_xlsx

urlpatterns = [
    path('', staff_member_required(MasterDataHomeView.as_view(), login_url='login_admin'), name='md_home'),
    path('customer/new/', staff_member_required(MasterDataCustomerCreateView.as_view(), login_url='login_admin'), name='md_customer_input'),
    path('customer/list/', staff_member_required(MasterDataCustomerListView.as_view(), login_url='login_admin'), name='md_customer_list'),
    path('customer/import_xlsx/', staff_member_required(import_md_customer_xlsx, login_url='login_admin'), name='import_md_customer_xlsx'),
    path('customer/<pk>/edit/', staff_member_required(MasterDataCustomerUpdateView.as_view(), login_url='login_admin'), name='md_customer_edit'),
    path('customer/<pk>/delete/', staff_member_required(MasterDataCustomerDeleteView.as_view(), login_url='login_admin'), name='md_customer_delete'),
    path('product/new/',  staff_member_required(MasterDataProductCreateView.as_view(), login_url='login_admin'), name='md_product_input'),
    path('product/list/',  staff_member_required(MasterDataProductListView.as_view(), login_url='login_admin'), name='md_product_list'),
    path('product/import_xlsx/', staff_member_required(import_md_product_xlsx, login_url='login_admin'), name='import_md_product_xlsx'),
    path('product/<pk>/edit/', staff_member_required(MasterDataProductUpdateView.as_view(), login_url='login_admin'), name='md_product_edit'),
    path('product/<pk>/delete/', staff_member_required(MasterDataProductDeleteView.as_view(), login_url='login_admin'), name='md_product_delete'),
]