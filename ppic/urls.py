from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .views import PPICHomeView
from .views import ChangeOrderListView, import_change_order_xlsx, delete_co, ajax_check_co

urlpatterns = [
    path('', PPICHomeView.as_view(), name='ppic_home'),
    path('co/list/', ChangeOrderListView.as_view(), name='change_order_list'),
    path('co/list/import_change_order_xlsx/', import_change_order_xlsx, name='import_change_order_xlsx'),
    path('co/list/delete_co/', delete_co, name='delete_co'),
    path('co/list/ajax_check/', ajax_check_co, name='check_co')
]