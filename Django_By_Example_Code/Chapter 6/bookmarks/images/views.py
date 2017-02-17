# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action
import redis
from django.conf import settings


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required
def image_create(request):
    """
    用JS书签创建的图片
    """
    if request.method == 'POST':
        # 已经发送表单
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # 表单数据有效
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # 指定当前用户到图片
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')
            # 重定向到图片detail
            return redirect(new_item.get_absolute_url())
    else:
        # 通过request.GET创建表单
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images',
                                                        'form': form}) #render的用法


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # 递增views
    total_views = r.incr('image:{}:views'.format(image.id))
    # 递增ranking
    r.zincrby('image_ranking', image.id, 1)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image,
                   'total_views': total_views}) #render的用法


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id') #id的用法
    action = request.POST.get('action') #action的用法
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id) #objects.get的用法
            if action == 'like':
                image.users_like.add(request.user) #users_like.add的用法
                create_action(request.user, 'likes', image) #创建action
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'}) #点击按钮后status是ok
        except:
            pass
    return JsonResponse({'status':'ko'}) #没点击按钮,status是ko


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8) #每页显示8张图片
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # page不是整数时,显示page(1)
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # 如果request是AJAX,页面超过范围
            return HttpResponse('')
        # 页面超过范围
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images}) #render的用法
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images}) #render的用法


@login_required
def image_ranking(request):
    # 图片排序的字典,image_ranking在每次请求image_detail时递增
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # 被查看最多的图片
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id)) #sort和lambda的用法
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed}) #render的用法
