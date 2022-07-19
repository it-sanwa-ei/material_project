from django.contrib import admin

# Register your models here.
from .models import ChangeOrder

admin.site.register(ChangeOrder, admin.ModelAdmin)