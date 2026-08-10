from django.contrib import admin

from .models import Advertisement

# Register your models here.
@admin.register(Advertisement)
class Adminfieldsets(admin.ModelAdmin):
    list_display = ("title", "service", "promotion_channel", "budget")
    search_fields = ("title", "service")
    list_filter = ("title", "service", "promotion_channel","budget")
    list_per_page = 25
