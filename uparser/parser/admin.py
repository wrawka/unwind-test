from django.contrib import admin

from parser.models import OrderLine


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    pass
