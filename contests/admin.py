# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Platform, Contest

# Register your models here.
admin.site.register(Platform)
admin.site.register(Contest)
