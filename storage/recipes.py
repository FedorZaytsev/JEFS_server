import json
import collections
import requests
import pickle
import csv
import os
from django.conf import settings

meal_types = {0: 'breakfast', 1: 'lunch', 2: 'dinner'}
Recipe = collections.namedtuple('Recipe', 'id title ingredients image vegetarian vegan cuisines glutenFree')


class RecipeAPI:
    """This class poses queries to the recipes API"""

    def __init__(self):
        self.headers = {"X-RapidAPI-Key": "229abf5047msh0496afd1b8be392p17c215jsn41d9d4524130"}
        self.url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"

    def get_random_recipes(self, number):
        params = {'number': number}
        r = requests.get(self.url + 'random', headers=self.headers, params=params)
        return r.json()

    def search_meal_plan_by_calories(self, calories, time_frame='daily'):
        params = {'targetCalories': calories, 'timeFrame': time_frame}
        r = requests.get(self.url + 'mealplans/generate', headers=self.headers, params=params)
        return r.json()

    def get_recipes_by_ids(self, ids):
        params = {'ids': ids}
        r = requests.get(self.url + 'informationBulk', headers=self.headers, params=params)
        return r.json()


class RecipeAPIRetriever:
    """ This class uses the RecipeAPI class to extract json data from the recipe API and to create
        the Recipe data required from our application."""

    def __init__(self):
        self.recipe_api = RecipeAPI()

    def retrieve_random_recipes(self, number):
        random_recipes = parse_recipes_json(self.recipe_api.get_random_recipes(number)['recipes'])
        return random_recipes

    def retrieve_recipes_by_id(self, ids):
        recipes = self.recipe_api.get_recipes_by_ids(','.join(map(str, ids)))
        return parse_recipes_json(recipes)

    def retrieve_meal_plans(self, calories=2000):
        daily_meal_plan = self.recipe_api.search_meal_plan_by_calories(calories, 'daily')
        return daily_meal_plan

    def retrieve_recipe_data(self, calories=2000, count=1):
        daily_meal_plans = []
        recipes = []
        for _ in range(count):
            daily_meal_plan = self.retrieve_meal_plans(calories)
            ids = [meal['id'] for meal in daily_meal_plan['meals']]
            recipes.append(self.retrieve_recipes_by_id(ids))
            daily_meal_plans.append(daily_meal_plan)
        return daily_meal_plans, recipes


class RecipeDiskRetriever:
    """ This class retrieves toy data from disk."""

    def retrieve_random_recipes(self):
        with open(os.path.join(settings.TOY_DATA_FOLDER, 'to_show_to_the_user/random_recipes.pkl'), 'rb') as f:
            random_recipes = pickle.load(f)
        return random_recipes

    def retrieve_recipes(self):
        with open(os.path.join(settings.TOY_DATA_FOLDER, 'by_calories_retrieval/recipes_infos.pkl'), 'rb') as f:
            recipes = pickle.load(f)
        return recipes

    def retrieve_meal_plans(self):
        with open(os.path.join(settings.TOY_DATA_FOLDER, 'by_calories_retrieval/daily_meal_plans.json')) as f:
            daily_meal_plan = json.load(f)
        return daily_meal_plan

    def retrieve_recipe_data(self):
        return self.retrieve_meal_plans(), self.retrieve_recipes()

    def retrieve_recipes_by_user(self):
        with open(os.path.join(settings.TOY_DATA_FOLDER, 'user_ingreds_1.pkl'), 'rb') as f:
            user_recipes = pickle.load(f)
        return user_recipes


def parse_recipes_json(recipes_json):
    """Parse recipes json as return by the Recipe API.
        Extract only the required fields.
        Return: a list of Recipe objects."""
    recipe_ids_to_recipe = {}
    for recipe_json in recipes_json:
        ingredients = extract_ingredients(recipe_json['extendedIngredients'])
        image = ""
        if 'image' in recipe_json:
            image = recipe_json['image']
        recipe = Recipe(id=recipe_json['id'], title=recipe_json['title'], ingredients=ingredients, image=image,
                        vegetarian=recipe_json['vegetarian'], glutenFree=recipe_json['glutenFree'],
                        vegan=recipe_json['vegan'], cuisines=recipe_json['cuisines'])
        recipe_ids_to_recipe[recipe_json['id']] = recipe
    return recipe_ids_to_recipe


def extract_ingredients(ingredients):
    """Extract ingredients names from ingredients json as returned by recipe API."""
    return [ingr['name'] for ingr in ingredients]


def group_recipes_by_meal_type(daily_meal_plans):
    """
    Group recipes ids by meal type (breakfast, lunch, dinner)
    :param daily_meal_plans: meal plans json as returned by recipe API.
    :return: a dict from meal type to list of recipe ids.
    """
    mealtype_to_recipeid = collections.defaultdict(list)
    for meal_plan in daily_meal_plans:
        meals = meal_plan['meals']
        for i, meal in enumerate(meals):
            mealtype_to_recipeid[meal_types[i]].append(meal['id'])
    return mealtype_to_recipeid


def get_recipe_data_by_calories(calories, count=1, use_toy_data=True):
    """
    Given a specific amount of calories, retrieve daily meals from recipe API and group recipes by meal type
    :param calories: max calories content for each recipe.
    :param count: number of recipes to retrieve.
    :use_toy_data: if True use the toy data in the folder ../sample_data, otherwise hit the actual recipe API.
    :return:
            mealtype_to_recipeid: dict of meal type to list of recipes ids.
            recipe_ids_to_recipe: dict of recipe id to recipe object.
    """
    if use_toy_data:
        retriever = RecipeDiskRetriever()
        daily_meal_plans, recipes = retriever.retrieve_recipe_data()
    else:
        retriever = RecipeAPIRetriever()
        daily_meal_plans, recipes = retriever.retrieve_recipe_data(calories=calories, count=count)
    mealtype_to_recipeid = group_recipes_by_meal_type(daily_meal_plans)
    rec_ids_to_recipe = {}
    for dict_entries in recipes:
        rec_ids_to_recipe.update(dict_entries)
    return mealtype_to_recipeid, rec_ids_to_recipe


def get_user_recipe_data(userId, use_toy_data=True):
    """ Get the favorite resipes from a user.
    if use_toy_data, get the toy recipes from disk. Otherwise, get them from the db."""
    if use_toy_data:
        retriever = RecipeDiskRetriever()
        return retriever.retrieve_recipes_by_user()
    return None


def get_random_recipe_data(number=10, use_toy_data=True, to_json = False):
    """ Get random recipe data in order to show to the user. Then the user selects those that he prefers."""
    if use_toy_data:
        retriever = RecipeDiskRetriever()
        random_recipes = retriever.retrieve_random_recipes()
    else:
        retriever = RecipeAPIRetriever()
        random_recipes = retriever.retrieve_random_recipes(number)
    recipes = parse_recipes_json(random_recipes)
    if to_json: return recipes_list_to_dicts(recipes)
    return recipes


def recipes_list_to_dicts(recipes_list):
    return [recipe._asdict() for recipe in recipes_list]


def get_unique_ingredients(ingredients_path='../sample_data/ingredients.csv'):
    with open(ingredients_path, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)
        names = [row[0] for row in csv_reader]
    return list(names)


def get_unique_cuisines():
    return ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', \
            'french', 'italian', 'mexican', 'spanish', 'middle', 'eastern', 'jewish', 'american', 'cajun', 'southern', \
            'greek', 'german', 'nordic', 'eastern', 'european', 'caribbean', 'latin']


def get_unique_diets():
    return ['pescatarian', 'lacto', 'vegetarian', 'lacto ovo vegetarian', 'vegan', 'vegetarian', 'gluten free',
            'grain free', 'dairy free', 'high protein', 'low sodium', 'low carb', 'Paleo', 'Primal']
