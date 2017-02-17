# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt #避免Django获取csrf
def payment_done(request):
    return render(request, 'payment/done.html') #render的用法


@csrf_exempt #避免Django获取csrf
def payment_canceled(request):
    return render(request, 'payment/canceled.html') #render的用法
    

def payment_process(request):
    order_id = request.session.get('order_id') #session.get的用法
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host() #get_host的用法

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')), #quantize的用法
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')), #reverse的用法
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict) #initial的用法
    return render(request, 'payment/process.html', {'order': order,
                                                    'form':form}) #render的用法
