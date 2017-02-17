# -*- coding: utf-8 -*-
import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv') #HttpResponse,content_type的用法
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name) #attachment的用法
    writer = csv.writer(response) #csv.writer的用法

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] # .model._meta.get_fields的用法, if not...and not的用法
    # 标题行
    writer.writerow([field.verbose_name for field in fields]) #writerow的用法
    # 数据行
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name) #getattr的用法
            if isinstance(value, datetime.datetime): #isinstance的用法
                value = value.strftime('%d/%m/%Y') #strftime的用法
            data_row.append(value) #append的用法
        writer.writerow(data_row) #writerow的用法
    return response #HttpResponse对象
export_to_csv.short_description = 'Export to CSV' #short_description的用法


def order_detail(obj):
    return '<a href="{}">View</a>'.format(reverse('orders:admin_order_detail',
                                                  args=[obj.id])) #reverse, args的用法
order_detail.allow_tags = True #allow_tags的用法

def order_pdf(obj):
    return '<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf',
                                                 args=[obj.id])) #reverse, args的用法
order_pdf.allow_tags = True #allow_tags的用法
order_pdf.short_description = 'PDF bill' #short_description的用法


class OrderItemInline(admin.TabularInline): #TabularInline的用法
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'first_name',
                    'last_name',
                    'email',
                    'address',
                    'postal_code',
                    'city',
                    'paid',
                    'created',
                    'updated',
                    order_detail,
                    order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline] #inlines的用法
    actions = [export_to_csv] #action的用法

admin.site.register(Order, OrderAdmin) #在admin注册Order
