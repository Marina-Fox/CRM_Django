from django.contrib import admin

from .models import Contracts


# Register your models here.
@admin.register(Contracts)
class AdminContracts(admin.ModelAdmin):
    list_display = ("title", "service", "start_date", "end_date", "cost")
    readonly_fields = ("start_date",)
    search_fields = ("title", "service", "start_date", "end_date")
    list_filter = ("title", "service", "start_date", "end_date", "cost")
    list_per_page = 25
