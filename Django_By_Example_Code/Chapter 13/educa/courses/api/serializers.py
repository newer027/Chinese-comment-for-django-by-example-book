# -*- coding: utf-8 -*-
from rest_framework import serializers
from ..models import Subject, Course, Module, Content


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'title', 'slug')


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render() #RelatedField, render的用法


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True) #read_only的用法,引用RelatedField
    class Meta:
        model = Content
        fields = ('order', 'item')


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('order', 'title', 'description')


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True) #嵌套的modules

    class Meta:
        model = Course
        fields = ('id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules')


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True) #嵌套的modules
    class Meta:
        model = Module
        fields = ('order', 'title', 'description', 'contents')


class CourseWithContentsSerializer(CourseSerializer):
    #ModuleWithContentsSerializer的fields包括contents, contents的fields包括order和item
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules')
