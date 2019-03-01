from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.views import View
from .models import *
from django.forms.models import model_to_dict
import time
from . import recommendations

import json

class StepCountView(View):
	@staticmethod
	def put(request, userId=None):
		body = None
		try:
			body = json.loads(request.body.decode('utf-8'))
		except json.decoder.JSONDecodeError as e:
			return HttpResponseBadRequest('Invalid json: {}'.format(e))


		step = StepCount(
			userId=userId, 
			stepCount=body['count'], 
			timestamp=int(time.time()),
		)
		step.save()

		return HttpResponse()

class LocationView(View):
	@staticmethod
	def put(request, userId=None):
		body = None
		try:
			body = json.loads(request.body.decode('utf-8'))
		except json.decoder.JSONDecodeError as e:
			return HttpResponseBadRequest('Invalid json: {}'.format(e))

		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		step = Locations(
			userId=usr, 
			longitude=body['longitude'], 
			latitude=body['latitude'], 
			timestamp=int(time.time()),
		)
		step.save()


		for e in Locations.objects.all():
			print("Locations new", model_to_dict(e))

		return HttpResponse()


class UserView(View):
	@staticmethod
	def put(request, userId=None):
		body = None
		try:
			body = json.loads(request.body.decode('utf-8'))
		except json.decoder.JSONDecodeError as e:
			return HttpResponseBadRequest('Invalid json: {}'.format(e))


		usr = User(id=userId, **body)
		usr.save()
		return HttpResponse()

	@staticmethod
	def get(request, userId):
		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		print("usr {} type {}".format(usr, type(usr)))

		return JsonResponse(model_to_dict(usr))

	@staticmethod
	def post(request, userId):
		body = None
		try:
			body = json.loads(request.body.decode('utf-8'))
		except json.decoder.JSONDecodeError as e:
			return HttpResponseBadRequest('Invalid json: {}'.format(e))


		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		for k, v in body.items():
			setattr(usr, k, v)

		usr.save()

		return HttpResponse()


class WorkoutRecommendation(View):
	@staticmethod
	def get(request, userId=None):
		step_count = StepCount.objects.filter(userId=userId)
		step_count = [model_to_dict(e) for e in step_count]
		locations = Locations.objects.filter(userId=userId)
		locations = [model_to_dict(e) for e in locations]
		return JsonResponse({
			'result': recommendations.recommend_workout(userId, step_count=step_count, locations=locations)
		})


class RecepiesRecommendation(View):
	@staticmethod
	def get(request, userId=None):
		step_count = StepCount.objects.filter(userId=userId)
		step_count = [model_to_dict(e) for e in step_count]
		locations = Locations.objects.filter(userId=userId)
		locations = [model_to_dict(e) for e in locations]
		return JsonResponse({
			'result': recommendations.recommend_recepies(userId, step_count=step_count, locations=locations)
		})

