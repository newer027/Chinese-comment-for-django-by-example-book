# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        #重新定义get_queryset,筛选published的对象
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    #草稿和已发布
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #SlugField和unique_for_date的用法
    author = models.ForeignKey(User, related_name='blog_posts') #ForeignKey和related_name的用法
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) #auto_now_add的用法,和auto_now的区别
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') #CharField和choices的用法

    objects = models.Manager() # The default manager.
    published = PublishedManager() # PublishedManager的用法

    tags = TaggableManager() #TaggableManager的用法

    class Meta:
        ordering = ('-publish',) #ordering的用法,-表示倒序

    def __str__(self):
        return self.title #__str__的用法

    def get_absolute_url(self): #get_absolute_url和reverse的用法
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments') #ForeignKey和related_name的用法
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',) #ordering的用法

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post) #__str__的用法
