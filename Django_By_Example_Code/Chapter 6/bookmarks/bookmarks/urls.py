# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)), #include的用法
    url(r'^account/', include('account.urls')),
    url(r'^images/', include('images.urls', namespace='images')),
    # python社交认证
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
]

# DEBUG时/media生效
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)