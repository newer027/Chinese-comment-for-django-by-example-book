# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    # 设置admin的Post
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
# 在admin注册Post
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    # 设置admin的Comment
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
# 在admin注册Comment
admin.site.register(Comment, CommentAdmin)
