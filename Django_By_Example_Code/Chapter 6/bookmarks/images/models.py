# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created') #ForeignKey和related_name的用法
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField() #URLField的用法
    image = models.ImageField(upload_to='images/%Y/%m/%d') #upload_to的用法
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True) #ManyToManyField的用法

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) #slugify的用法
        super(Image, self).save(*args, **kwargs) #生成slug后重写save

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug]) #reverse的用法
