# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Post

# sitemaps的配置
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish