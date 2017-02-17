# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists() #filter.exists的用法,检查是不是学生
