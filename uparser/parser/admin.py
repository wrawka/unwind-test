from django.contrib import admin

from parser.models import OrderLine


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = (
        'line_no',
        'order_no',
        'due_date',
        'value_usd',
        'value_rub'
    )
    search_fields = ('order_no', 'due_date')
    fields = (
        ('line_no', 'order_no'),
        'due_date',
        ('value_usd', 'value_rub')
    )
