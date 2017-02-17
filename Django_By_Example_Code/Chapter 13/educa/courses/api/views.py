# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer
from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer #ListAPIView, serializer_class的用法


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer #RetrieveAPIView, serializer_class的用法


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer #ReadOnlyModelViewSet, serializer_class的用法

    @detail_route(methods=['post'],
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated]) #post的用法,IsAuthenticated的用法
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user) #add(request.user)的用法
        return Response({'enrolled': True}) #Response的用法

    @detail_route(methods=['get'],
                  serializer_class=CourseWithContentsSerializer,
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated, IsEnrolled]) #post的用法,IsAuthenticated, IsEnrolled的用法
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs) #retrieve的用法


# class CourseEnrollView(APIView):
#    authentication_classes = (BasicAuthentication,)
#    permission_classes = (IsAuthenticated,)
#
#    def post(self, request, pk, format=None):
#        course = get_object_or_404(Course, pk=pk)
#        course.students.add(request.user)
#        return Response({'enrolled': True})
