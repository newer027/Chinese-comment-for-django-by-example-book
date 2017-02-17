# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) #forms.PasswordInput的用法


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput) #forms.PasswordInput的用法
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput) #二次输入密码

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data #cleaned_data的用法
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.') #ValidationError的用法
        return cd['password2'] #没有ValidationError时执行


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email') #ModelForm的用法


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo') #ModelForm的用法
