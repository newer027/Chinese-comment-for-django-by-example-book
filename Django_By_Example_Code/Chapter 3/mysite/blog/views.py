# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count

from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from haystack.query import SearchQuerySet


def post_list(request, tag_slug=None):
    #Post清单
    object_list = Post.published.all()
    tag = None

    #如果有tag_slug,tag_slug=>tag=>object_list
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    #分页
    paginator = Paginator(object_list, 3) # 每页3篇文章
    #request.GET的用法,Paginator生成'page'
    page = request.GET.get('page')
    try:
        #当前页面的posts
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数,显示第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果page太大,给出最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag}) #render的用法


#django的ListView的用法,是对post_list的简化
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    # 从Post的slug,publish属性获得当前文章
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # 当前文章的所有评论
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # 从表单获取评论
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # 创建评论对象,但不提交保存
            new_comment = comment_form.save(commit=False)
            # 指定当前评论到当前文章
            new_comment.post = post
            # 保存评论到数据库
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 相似的文章清单
    post_tags_ids = post.tags.values_list('id', flat=True) #values_list的用法
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) #filter和exclude的用法
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-publish')[:4] #annotate的用法,same_tags是相同tags的数量
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts}) #render的用法



def post_share(request, post_id):
    # 通过id获取文章
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # 提交了表单
        form = EmailPostForm(request.POST) #EmailPostForm来自blog/forms.py
        if form.is_valid():
            # 表单内容通过验证
            cd = form.cleaned_data #cleaned_data的用法
            post_url = request.build_absolute_uri(post.get_absolute_url()) #build_absolute_uri的用法
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title) #format和cd的用法
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments']) #format和cd的用法
            send_mail(subject, message, 'admin@myblog.com', [cd['to']]) #send_mail的用法
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_search(request):
    form = SearchForm()
    # request.GET的用法
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all() #SearchQuerySet的用法
            # 对所有结果计数
            total_results = results.count()
    return render(request, 'blog/post/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results})
