from django.contrib import admin

from .models import Customers


# Register your models here.
@admin.register(Customers)
class AdminCustomers(admin.ModelAdmin):
    list_display = ("lead", "contract")
    readonly_fields = ("lead", "contract")
    search_fields = ("lead", "contract")
    list_filter = ("lead", "contract")
    list_per_page = 25
