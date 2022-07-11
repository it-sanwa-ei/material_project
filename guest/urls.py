from django.urls import path

from .views import GuestHomeTemplateView
from .views import AboutUsTemplateView, CompanyStructureTemplateView
from .views import ProductsTemplateView, InjectionMoldingTemplateView, MoldMakingTemplateView, MoldMaintenanceTemplateView, QualityControlTemplateView
from .views import CareerTemplateView
from .views import ContactUsTemplateView, guest_send_email ,GuestSendMailSuccessTemplateView

urlpatterns = [
    path('', GuestHomeTemplateView.as_view(), name='guest_home'),
    path('company/about_us/', AboutUsTemplateView.as_view(), name='guest_about_us'),
    path('company/structure/', CompanyStructureTemplateView.as_view(), name='guest_company_structure'),
    path('services/products/', ProductsTemplateView.as_view(), name='guest_products'),
    path('services/im/', InjectionMoldingTemplateView.as_view(), name='guest_injection_molding'),
    path('services/ms/', MoldMakingTemplateView.as_view(), name='guest_mold_making'),
    path('services/mm/', MoldMaintenanceTemplateView.as_view(), name='guest_mold_maintenance'),
    path('services/qc/', QualityControlTemplateView.as_view(), name='guest_quality_control'),
    path('career/', CareerTemplateView.as_view(), name='guest_career'),
    path('contactus/', ContactUsTemplateView.as_view(), name='guest_contact_us'),
    path('contactus/sending-email', guest_send_email, name='guest_send_email'),
    path('contactus/sending-email-success/', GuestSendMailSuccessTemplateView.as_view(), name='guest_email_success'),
]