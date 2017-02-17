# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin


class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)} #get_prepopulated_fields的用法

admin.site.register(Category, CategoryAdmin) #在admin注册Category


class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)} #get_prepopulated_fields的用法

admin.site.register(Product, ProductAdmin) #在admin注册Product
