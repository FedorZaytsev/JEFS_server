from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.views import View
from .models import *
from django.forms.models import model_to_dict
import time
from . import recommendations
from .recipes import get_random_recipe_data, recipes_list_to_dicts
import json
import datetime
import random
import numpy as np

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

		body['cuisine'] = json.dumps(body.get('cuisine', []))
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

		usr = model_to_dict(usr)
		usr['cuisine'] = json.loads(usr.get('cuisine', '[]'))

		return JsonResponse(usr)

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
			if k == 'cuisine':
				v = json.dumps(v)
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
		return JsonResponse({
			'result': recommendations.recommend_recipes(userId)
		})

def addFakeData(recipe):
	recipe.calories = random.randrange(50, 600)
	if recipe.vegetarian:
		recipe.calories = int(recipe.calories * 0.8)
	elif recipe.vegan:
		recipe.calories = int(recipe.calories * 0.6)

	recipe.fat = random.randrange(1, 30)
	recipe.carb = int(recipe.fat + random.randrange(15, 30)/10)
	if recipe.vegetarian:
		recipe.fat = int(recipe.fat * 0.2)
	elif recipe.vegan:
		recipe.fat = int(recipe.fat * 0.1)

	if recipe.vegetarian:
		recipe.carb = int(recipe.carb * 0.2)
	elif recipe.vegan:
		recipe.carb = int(recipe.carb * 0.1)

	recipe.protein = random.randrange(1, 100)
	if recipe.vegetarian:
		recipe.protein = int(recipe.protein * 0.9)
	elif recipe.vegan:
		recipe.protein = int(recipe.protein * 0.8)



class RecipesView(View):
	@staticmethod
	def get(request, userId=None):
		count = int(request.GET.get('count', '10'))
		response = get_random_recipe_data(count, to_json=True)

		for e in response:
			print('e', e)
			recipe = Recipe(
				**e)
			addFakeData(recipe)
			recipe.save()

		return JsonResponse({
			'result': response
		})

class RecipeLikeView(View):
	@staticmethod
	def post(request, userId=None, recipeId=None):
		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		recipe = None
		try:
			recipe = Recipe.objects.get(pk=recipeId)
		except Recipe.DoesNotExist:
			raise Http404("Recipe does not exist")

		like = LikedRecepy(
			userId=usr,
			recipeId=recipe,
			timestamp=datetime.datetime.now()
		)
		like.save()

		return HttpResponse()


class UserProfile(View):
	@staticmethod
	def post(request, userId=None):
		timestamp = request.GET.get('date')
		body = None
		try:
			body = json.loads(request.body.decode('utf-8'))
		except json.decoder.JSONDecodeError as e:
			return HttpResponseBadRequest('Invalid json: {}'.format(e))


		timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		hist = UserHistory(
			userId=usr,
			weight=body['weight'],
			height=body['height'],
			timestamp=timestamp
		)

		hist.save()

		return HttpResponse()

	@staticmethod
	def get(request, userId=None):
		fromdate = request.GET.get('from')
		fromdate = datetime.datetime.strptime(fromdate, "%Y-%m-%d")

		todate = request.GET.get('to')
		todate = datetime.datetime.strptime(todate, "%Y-%m-%d")

		print("from", fromdate)
		print("to", todate)

		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		res = UserHistory.objects.filter(timestamp__gte=fromdate).filter(timestamp__lte=todate).order_by('timestamp')
		res = [model_to_dict(e) for e in res]

		return JsonResponse({
			'response': res,
		})



class ConsumedCalories(View):
	@staticmethod
	def get(request, userId=None):
		fromdate = request.GET.get('from')
		fromdate = datetime.datetime.strptime(fromdate, "%Y-%m-%d")

		todate = request.GET.get('to')
		todate = datetime.datetime.strptime(todate, "%Y-%m-%d")

		print("from", fromdate)
		print("to", todate)

		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		res = LikedRecepy.objects.filter(userId=usr).filter(timestamp__gte=fromdate).filter(timestamp__lte=todate)

		daily = {}

		for e in res:
			timestamp = e.timestamp.strftime("%Y-%m-%d")
			daily[timestamp] = float(daily.get(timestamp, 0) + e.recipeId.calories)

		return JsonResponse({
			'response': {
				'overall': np.sum(list(daily.values())),
				'daily': daily
			}
		})


class ConsumedNutriens(View):
	@staticmethod
	def get(request, userId=None):
		fromdate = request.GET.get('from')
		fromdate = datetime.datetime.strptime(fromdate, "%Y-%m-%d")

		todate = request.GET.get('to')
		todate = datetime.datetime.strptime(todate, "%Y-%m-%d")

		print("from", fromdate)
		print("to", todate)

		usr = None
		try:
			usr = User.objects.get(pk=userId)
		except User.DoesNotExist:
			raise Http404("User does not exist")

		res = LikedRecepy.objects.filter(userId=usr).filter(timestamp__gte=fromdate).filter(timestamp__lte=todate)

		daily_fat = {}
		daily_carb = {}
		daily_protein = {}

		for e in res:
			timestamp = e.timestamp.strftime("%Y-%m-%d")
			daily_fat[timestamp] = float(daily_fat.get(timestamp, 0) + e.recipeId.fat)
			daily_carb[timestamp] = float(daily_carb.get(timestamp, 0) + e.recipeId.carb)
			daily_protein[timestamp] = float(daily_protein.get(timestamp, 0) + e.recipeId.protein)

		return JsonResponse({
			'response': {
				'fat': {
					'overall': np.sum(list(daily_fat.values())),
					'daily': daily_fat,
				},
				'carb': {
					'overall': np.sum(list(daily_carb.values())),
					'daily': daily_carb,
				},
				'protein': {
					'overall': np.sum(list(daily_protein.values())),
					'daily': daily_protein,
				},
			}
		})













