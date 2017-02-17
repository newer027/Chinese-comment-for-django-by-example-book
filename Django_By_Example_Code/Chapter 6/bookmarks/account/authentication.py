# -*- coding: utf-8 -*-
from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    用邮件验证用户
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username) #objects.get的用法
            if user.check_password(password): #检查密码
                return user
            return None
        except User.DoesNotExist: #用户不存在
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id) #用user_id获取user
        except User.DoesNotExist:
            return None