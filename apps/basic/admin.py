from django.contrib import admin
from apps.basic.models import ClickOrder
# Register your models here.

@admin.register(ClickOrder)
class ClickOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount']
    list_display_links = ['id', 'amount', ]

    save_on_top = True