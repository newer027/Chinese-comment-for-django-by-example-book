# -*- coding: utf-8 -*-
import os
from celery import Celery
from django.conf import settings

# Django默认设置,用于celery程序
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) #lambda的用法