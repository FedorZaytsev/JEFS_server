# Recommendations
from .places import gmaps, weatherAPI
from .recommend_helper import *
from .recipes import *
import json

def recommend_workout(userId, **kwargs):
	print("Start recommendation engine for user {}. Arguments {}".format(userId, kwargs))
	print(kwargs)
	# example for to find nearby places
	for location in kwargs['locations']:
		places = gmaps.getNearby(location['latitude'], location['longitude'], radius=20)
		print(location, ':', json.dumps(places, indent=2))


	# example how to get weather
	weather = weatherAPI.getCurrentWeather()
	print('weather', weather)

	return []

def recommend_recipes(userId, **kwargs):

	print("Start recommendation engine for user {}. Arguments {}".format(userId, kwargs))

	# get user info (weight etc) from db.
	user_info = get_user(userId, toy_user = True)
	# get user favorite recipes data from db
	user_recipes = get_user_recipe_data(userId, use_toy_data=True)
	# based on user current weight and current goal, compute daily calories intake
	cals_to_take = compute_daily_calories_intake(user_info)
	# get meal plans with maximum number of calories cals_to_take.
	mealtype_to_recipeid, rec_ids_to_recipe  = get_recipe_data_by_calories(cals_to_take, count = 10, use_toy_data= True)

	# load vocabulary of features based on which you make user/recipes profiles.
	features_vocab, features_vocab_inv = load_features_vocabs()
	# create user vector space profile
	user_profile = create_user_profile(user_recipes, features_vocab_inv)
	# create recipes vector space models
	recipes_profiles = create_recipes_profiles(rec_ids_to_recipe, features_vocab_inv)

	# for each meal type (breakfast, lunch, dinner) find the 7 recipes that are most similar to the user profile
	most_similar_per_meal_type = {}
	for meal_type in meal_types.values():
		meal_type_recipes = mealtype_to_recipeid[meal_type]
		meal_type_recipes_profiles = [(rec_id, recipes_profiles[rec_id]) for rec_id in meal_type_recipes]
		most_similar_per_meal_type[meal_type] = find_k_most_similar_recipes(user_profile, meal_type_recipes_profiles, 7)
	weekly_recommendations = create_weekly_recommendations(most_similar_per_meal_type, rec_ids_to_recipe,
														   recipes_to_dict = True)
	return weekly_recommendations

