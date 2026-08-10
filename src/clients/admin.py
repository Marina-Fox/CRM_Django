from django.contrib import admin

from .models import Lead

# Register your models here.
@admin.register(Lead)
class AdminLead(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "patronymic", "phone", "email")
    search_fields = ("first_name", "last_name", "patronymic", "phone", "email")
    list_filter = ("first_name", "last_name", "patronymic")
    list_per_page = 25
