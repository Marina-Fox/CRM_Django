from django.contrib import admin
from django.utils.text import Truncator

from .models import Services
# Register your models here.

@admin.register(Services)
class AdminServices(admin.ModelAdmin):
    list_display = ("title", "created_at", "cost", "short_description")
    readonly_fields  = ("created_at",)
    search_fields = ("title",)
    list_filter = ("title", "created_at", "cost")
    ordering = ("created_at",)
    list_per_page = 25

    def short_description(self, obj):
        if not obj.description:
            return "-"
        return Truncator(obj.description).chars(100)
