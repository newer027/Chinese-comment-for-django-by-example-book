# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


translatable_models = {
    'Category': ['name', 'slug'],
    'Product': ['name', 'slug', 'description'],
}


def forwards_func(apps, schema_editor):
    for model, fields in translatable_models.items():
        Model = apps.get_model('shop', model) #get_model的用法
        ModelTranslation = apps.get_model('shop', '{}Translation'.format(model))

        for obj in Model.objects.all():
            translation_fields = {field: getattr(obj, field) for field in fields} #getattr的用法
            translation = ModelTranslation.objects.create(
                            master_id=obj.pk,
                            language_code=settings.LANGUAGE_CODE,
                            **translation_fields) #objects.create的用法


def backwards_func(apps, schema_editor):
    for model, fields in translatable_models.items():
        Model = apps.get_model('shop', model) #get_model的用法
        ModelTranslation = apps.get_model('shop', '{}Translation'.format(model))

        for obj in Model.objects.all():
            translation = _get_translation(obj, ModelTranslation) #_get_translation的用法
            for field in fields:
                setattr(obj, field, getattr(translation, field)) #setattr, getattr的用法
            obj.save()


def _get_translation(obj, MyModelTranslation):
    translations = MyModelTranslation.objects.filter(master_id=obj.pk) #master_id的用法
    try:
        # 默认翻译
        return translations.get(language_code=settings.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        return translations.get()


class Migration(migrations.Migration): #Migration, dependencies和operations的用法

    dependencies = [
        ('shop', '0002_add_translation_model'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
