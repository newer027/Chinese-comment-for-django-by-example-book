# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']

# 注册Image
admin.site.register(Image, ImageAdmin)
