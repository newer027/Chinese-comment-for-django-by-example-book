# -*- coding: utf-8 -*-
from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """
    订单创建后发送邮件通知
    """
    order = Order.objects.get(id=order_id) #objects.get的用法
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                             order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email]) #mail_sent是布尔值
    return mail_sent
