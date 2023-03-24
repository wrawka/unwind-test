from django.shortcuts import render, redirect
from django.db.models import Sum

from parser.models import OrderLine
from utils.loader import load2django

HEADER = [
    '№', 'заказ №', 'срок поставки', 'стоимость,$', 'стоимость в руб.'
]


def index(request):
    orders = OrderLine.objects.all()
    usd_total = orders.aggregate(Sum('value_usd')).get('value_usd__sum')
    context = {
        'header': HEADER,
        'usd_total': usd_total,
        'orders': orders
    }
    return render(request, 'index.html', context=context)


def refresh(request):
    load2django()
    return redirect(index)
