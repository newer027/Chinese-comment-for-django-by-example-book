# -*- coding: utf-8 -*-
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'
    verbose_name = 'Payment'

    def ready(self):
        # import signal handlers
        import payment.signals #signals的用法
