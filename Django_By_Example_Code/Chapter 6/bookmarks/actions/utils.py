# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    # 检查一分钟以内的类似action
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute) #created__gte, objects.filter的用法
    if target:
        target_ct = ContentType.objects.get_for_model(target) #objects.get_for_model的用法
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)

    if not similar_actions:
        # 没有发现similar_action
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False #存在similar_actions
