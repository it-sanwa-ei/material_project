from django.urls import path

from .views import RegisterView, LoginAdminView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login_admin/', LoginAdminView.as_view(), name='login_admin')
]