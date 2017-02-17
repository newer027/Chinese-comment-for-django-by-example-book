# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    verbose_name = 'Image bookmarks'

    def ready(self):
        # import signal handlers
        import images.signals #加载signals
