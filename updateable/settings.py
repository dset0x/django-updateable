# -*- coding: utf-8 -*-

from django.conf import settings

UPDATEABLE_REQUEST_OBJECT = getattr(settings, 'UPDATEABLE_REQUEST_OBJECT', '_updateable')
