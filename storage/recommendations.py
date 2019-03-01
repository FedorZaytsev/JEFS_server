# Recommendations

from .places import *
import json

def recommend_workout(userId, **kwargs):
	print("Start recommendation engine for user {}. Arguments {}".format(userId, kwargs))

	# example for to find nearby places
	for location in kwargs['locations']:
		places = gmaps.getNearby(location['latitude'], location['longitude'], radius=20)
		print(location, ':', json.dumps(places, indent=2))


	# example how to get weather
	weather = weatherAPI.getCurrentWeather()
	print('weather', weather)

	return []

def recommend_recepies(userId, **kwargs):
	print("Start recommendation engine for user {}. Arguments {}".format(userId, kwargs))
	return []

