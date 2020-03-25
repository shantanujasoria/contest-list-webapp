# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .contestscript import get_contests
from .models import Contest, Platform
from datetime import timedelta, datetime
from django.utils import timezone
# Create your views here.

def convert_time(n):
	sec = timedelta(seconds=n)
	d = datetime(1,1,1) + sec
	s = ""
	if d.day - 1 > 0:
		s += str(d.day-1) 
		if d.day - 1 == 1:
			s += " day, "
		else:
			s += " days, "
	if d.hour > 0:
		s += str(d.hour) + " hrs, "
	if d.minute > 0:
		s += str(d.minute) + " min, "
	if d.second > 0:
		s += str(d.second) + " sec, "
	return s.strip(', ')

def create_contests():
	contest_list = get_contests()
	for contest in contest_list:
		if Contest.objects.filter(event_link = contest['href'],event = ''.join([i if ord(i) < 128 else '' for i in contest['event']])).exists():
			cur = Contest.objects.get(event_link = contest['href'],event = ''.join([i if ord(i) < 128 else '' for i in contest['event']]))
			cur.start_time = datetime.strptime(contest['start'], '%Y-%m-%dT%H:%M:%S') + timedelta(minutes = 330)
			cur.end_time = datetime.strptime(contest['end'], '%Y-%m-%dT%H:%M:%S') + timedelta(minutes = 330)
			continue
		temp = Contest()
		temp.duration = convert_time(contest['duration'])
		try:
			temp.platform = Platform.objects.get(link=contest['resource']['name'])
		except:
			temp.platform = Platform.objects.get(name="Unknown")
			print(contest['resource']['name'])
		temp.event = ''.join([i if ord(i) < 128 else '' for i in contest['event']])
		temp.start_time = datetime.strptime(contest['start'], '%Y-%m-%dT%H:%M:%S') + timedelta(minutes = 330)
		temp.end_time = datetime.strptime(contest['end'], '%Y-%m-%dT%H:%M:%S') + timedelta(minutes = 330)
		temp.event_link = contest['href']
		temp.save()

def home(request):
	create_contests()
	contest_list = Contest.objects.all()
	past_contest = []
	present_contest = []
	future_contest = []
	for i in contest_list:
		if i.status() == 'Upcoming':
			future_contest.append(i)
		elif i.status() == 'Ongoing':
			present_contest.append(i)
		else:
			past_contest.append(i)
	past_contest.sort(key= lambda x:x.end_time)
	past_contest.reverse()
	present_contest.sort(key= lambda x:x.end_time)
	future_contest.sort(key= lambda x:x.start_time)
#	future_contest.reverse()
	return render(request, 'contests/home.html',{
			'upcoming_contests':future_contest,
			'ongoing_contests':present_contest,
			'past_contests':past_contest,
		})
