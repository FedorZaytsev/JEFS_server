from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from .models import *
from django.forms.models import model_to_dict
import time

import json

class StepCountView(View):
	@staticmethod
	def put(request, user_id=None):
		body = json.loads(request.body.decode('utf-8'))
		step = StepCount(
			user_id=user_id, 
			stepCount=body['count'], 
			timestamp=int(time.time()),
		)
		step.save()

		return HttpResponse()

class LocationView(View):
	@staticmethod
	def put(request, user_id=None):
		body = json.loads(request.body.decode('utf-8'))
		step = Locations(
			user_id=user_id, 
			longitude=body['longitude'], 
			latitude=body['latitude'], 
			timestamp=int(time.time()),
		)
		step.save()

		return HttpResponse()


class UserView(View):
	@staticmethod
	def put(request, user_id=None):
		body = json.loads(request.body.decode('utf-8'))
		usr = User(id=user_id, name=body['name'])
		usr.save()
		return HttpResponse()

	@staticmethod
	def get(request, user_id):
		usr = None
		try:
			usr = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		print("usr {} type {}".format(usr, type(usr)))

		return JsonResponse(model_to_dict(usr))