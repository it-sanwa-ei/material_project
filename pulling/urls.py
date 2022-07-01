from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .views import PullingHomeView
from .views import PullingCustomerCreateView, PullingCustomerListView, PullingCustomerUpdateView, PullingCustomerDeleteView
from .views import PullingProductCreateView, PullingProductListView, PullingProductUpdateView, PullingProductDeleteView
from .views import PullingLabelFormView, PullingLabelScanInView, PullingLabelScanOutView
from .views import TempScanInListView, TempScanInUpdateView, TempScanInDeleteView, ScanInListView, ScanOutListView
from .views import TempScanOutListView, TempScanOutUpdateView, TempScanOutDeleteView
from .views import PullingFinishGoodItemListView, FinishGoodStockListView
from .views import import_pulling_customer_xlsx, import_pulling_product_xlsx
from .views import pulling_label_form_ajax, pulling_label_pdf, pulling_label_in_decode, pulling_label_out_decode
from .views import scan_in_warehouse_db, scan_out_warehouse_db

urlpatterns = [
    path('', PullingHomeView.as_view(), name='pulling_home'),
    path('customer/new/', PullingCustomerCreateView.as_view(), name='pulling_customer_input'),
    path('customer/list/', PullingCustomerListView.as_view(), name='pulling_customer_list'),
    path('customer/import_xlsx/', staff_member_required(import_pulling_customer_xlsx, login_url='login_admin'), name='import_pulling_customer_xlsx'),
    path('customer/<int:pk>/edit/', staff_member_required(PullingCustomerUpdateView.as_view(), login_url='login_admin'), name='pulling_customer_edit'),
    path('customer/<int:pk>/delete/', staff_member_required(PullingCustomerDeleteView.as_view(), login_url='login_admin'), name='pulling_customer_delete'),
    path('product/new/', PullingProductCreateView.as_view(), name='pulling_product_input'),
    path('product/list/', PullingProductListView.as_view(), name='pulling_product_list'),
    path('product/import_xlsx/', staff_member_required(import_pulling_product_xlsx, login_url='login_admin'), name='import_pulling_product_xlsx'),
    path('product/<pk>/edit/', staff_member_required(PullingProductUpdateView.as_view(), login_url='login_admin'), name='pulling_product_edit'),
    path('product/<pk>/delete/', staff_member_required(PullingProductDeleteView.as_view(), login_url='login_admin'), name='pulling_product_delete'),
    path('label/new/', login_required(PullingLabelFormView.as_view(), login_url='login'), name='pulling_label_input'),
    path('label/new/auto-fill-ajax/', pulling_label_form_ajax, name='pulling_label_form_ajax'),
    path('label/new/pdf/', pulling_label_pdf, name='pulling_label_pdf'),
    path('scan-label/in/new/decode-qr/', pulling_label_in_decode, name='pulling_label_in_decode'),
    path('scan-label/in/new/', login_required(TempScanInListView.as_view(), login_url='login'), name='temp_scan_in'),
    path('scan-label/in/new/confirm/', login_required(scan_in_warehouse_db, login_url='login'), name='finish_good_in_warehouse'),
    path('scan-label/in/new/<int:pk>/edit/', login_required(TempScanInUpdateView.as_view(), login_url='login'), name='temp_scan_in_edit'),
    path('scan-label/in/new/<int:pk>/delete/', login_required(TempScanInDeleteView.as_view(), login_url='login'), name='temp_scan_in_delete'),
    path('scan-label/in/list/', login_required(ScanInListView.as_view(), login_url='login'), name='scan_in_list'),
    path('finish-good/log/', staff_member_required(PullingFinishGoodItemListView.as_view(), login_url='login_admin'), name='pulling_finish_good_item_list'),
    path('finish-good/list/', login_required(FinishGoodStockListView.as_view(), login_url='login'), name='finish_good_stock'),
    path('scan-label/out/new/decode-qr/', pulling_label_out_decode, name='pulling_label_out_decode'),
    path('scan-label/out/new/', login_required(TempScanOutListView.as_view(), login_url='login'), name='temp_scan_out'),
    path('scan-label/out/new/confirm/', login_required(scan_out_warehouse_db, login_url='login'), name='finish_good_out_warehouse'),
    path('scan-label/out/new/<int:pk>/edit/', login_required(TempScanOutUpdateView.as_view(), login_url='login'), name='temp_scan_out_edit'),
    path('scan-label/out/new/<int:pk>/delete/', login_required(TempScanOutDeleteView.as_view(), login_url='login'), name='temp_scan_out_delete'),
    path('scan-label/out/list/', login_required(ScanOutListView.as_view(), login_url='login'), name='scan_out_list'),
]