# -*- coding: utf-8 -*-
from django import forms
from .models import Comment


class EmailPostForm(forms.Form): #forms.Form的用法
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body') #ModleForm, Meta和fields的用法


class SearchForm(forms.Form):
    query = forms.CharField() #search.html中有 if "query" in request.GET
