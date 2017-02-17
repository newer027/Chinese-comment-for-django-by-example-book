# -*- coding: utf-8 -*-
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description') #表单的字段
        widgets = {
            'url': forms.HiddenInput,
        } #widget的用法

    def clean_url(self):
        url = self.cleaned_data['url'] #cleaned_data的用法
        valid_extensions = ['jpg', 'jpeg'] #有效的后缀列表
        extension = url.rsplit('.', 1)[1].lower() #rsplit的用法
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.') #ValidationError的用法
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False) #保存图片,不提交
        image_url = self.cleaned_data['url'] #cleaned_data的用法
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower()) #slugify和rsplit的用法

        # 从给定网址下载图片
        response = request.urlopen(image_url) #response的用法
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False) #ContentFile的用法

        if commit:
            image.save()
        return image
