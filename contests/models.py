# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Platform(models.Model):
	name = models.CharField(max_length=100)
	link = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Contest(models.Model):
	duration = models.CharField(max_length=100) 		# In hrs
	event = models.CharField(max_length=500)
	start_time = models.DateTimeField('Contest Start time', default=timezone.now)
	end_time = models.DateTimeField('Contest End time', default=timezone.now)
	event_link = models.CharField(max_length=500)
	platform = models.ForeignKey(Platform)

	def __str__(self):
		return self.event

	def status(self):
		if self.start_time > timezone.now():
			return "Upcoming"
		elif self.end_time >= timezone.now():
			return "Ongoing"
		else:
			return "Past"
