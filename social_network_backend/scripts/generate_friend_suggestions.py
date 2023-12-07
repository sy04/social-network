# -*- coding: utf-8 -*-

import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'social_network_backend.settings')
django.setup()

from account.models import User

users = User.objects.all()

for user in users:
  user.people_may_you_know.clear()

  print('Find friends for:', user)

  for friend in user.friends:
    print('Is friend with:', friend)

    for friendsfriend in friend.friends.all():
      if friendsfriend not in user.friends.all() and friendsfriend != user:
        user.people_may_you_know.add(friendsfriend)