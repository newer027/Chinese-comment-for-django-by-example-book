# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from parler.models import TranslatableModel, TranslatedFields #parler的用法


class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, db_index=True),
        slug = models.SlugField(max_length=200, db_index=True, unique=True)
    ) #TranslatableModel, TranslatedFields的用法

    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories' #复数

    def __str__(self):
        return self.name #__str__的用法

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug]) #get_absolute_url, reverse的用法


class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, db_index=True),
        slug = models.SlugField(max_length=200, db_index=True),
        description = models.TextField(blank=True)
    ) #TranslatableModel, TranslatedFields的用法
    category = models.ForeignKey(Category, related_name='products')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) #DecimalField的用法
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created',) #ordering的用法
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name #__str__的用法

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug]) #get_absolute_url, reverse的用法
