# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from common.decorators import ajax_required
from actions.models import Action
from actions.utils import create_action


def user_login(request):
    if request.method == 'POST': #提交登录信息后
        form = LoginForm(request.POST) #提交的信息
        if form.is_valid(): #提交的信息有效
            cd = form.cleaned_data #cleaned_data的用法
            user = authenticate(username=cd['username'], password=cd['password']) #验证用户和密码
            if user is not None: #用户存在
                if user.is_active: #激活的用户
                    login(request, user) #用户登录
                    return HttpResponse('Authenticated successfully') #登录成功
                else:
                    return HttpResponse('Disabled account') #失效的用户
            else:
                return HttpResponse('Invalid login') #无效的登录
    else:
        form = LoginForm() #提交的信息
    return render(request, 'account/login.html', {'form': form}) #render的用法


def register(request):
    if request.method == 'POST': #提交登录信息后
        user_form = UserRegistrationForm(request.POST) #提交的信息

        if user_form.is_valid(): #提交的信息有效
            # 创建一个新的用户对象,先不保存
            new_user = user_form.save(commit=False)
            # 设置用户密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存用户对象
            new_user.save()
            # 创建用户信息
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account') #创建action
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user}) #render的用法
    else:
        user_form = UserRegistrationForm() #提交的信息
    return render(request, 'account/register.html', {'user_form': user_form}) #render的用法


@login_required #需要登录
def edit(request):
    if request.method == 'POST': #提交登录信息后
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST) #用户表单
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES) #用户信息表单
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save() #如果表单都有效,保存表单
            messages.success(request, 'Profile updated successfully') #messages.success的用法
        else:
            messages.error(request, 'Error updating your profile') #messages.error的用法
    else:
        user_form = UserEditForm(instance=request.user) #用户表单
        profile_form = ProfileEditForm(instance=request.user.profile) #用户信息表单
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form}) #render的用法


@login_required #需要登录
def dashboard(request):
    # 其他用户所有action
    actions = Action.objects.all().exclude(user=request.user)
    # 用户关注的对象
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # 用户关注对象的action
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    # 显示前10个action
    actions = actions[:10]

    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions}) #render的用法


@login_required #需要登录
def user_list(request):
    users = User.objects.filter(is_active=True) #激活的用户
    return render(request, 'account/user/list.html', {'section': 'people',
                                                      'users': users}) #render的用法


@login_required #需要登录
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True) #get_object_or_404的用法
    return render(request, 'account/user/detail.html', {'section': 'people',
                                                        'user': user}) #render的用法

@ajax_required #用到ajax
@require_POST #装饰器的使用
@login_required #需要登录
def user_follow(request):
    user_id = request.POST.get('id') #用POST得到id
    action = request.POST.get('action') #用POST得到action
    if user_id and action: #user_id和action都有效
        try:
            user = User.objects.get(id=user_id) #objects.get的用法
            if action == 'follow': #action是follow
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user) #objects.get_or_create的用法
                create_action(request.user, 'is following', user) #创建action
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete() #action是unfollow
            return JsonResponse({'status':'ok'}) #follow/unfollow成功
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'}) #follow/unfollow不成功
    return JsonResponse({'status':'ko'}) #user_id和action不是都有效
