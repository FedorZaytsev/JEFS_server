"""Helper methods for the recommendation process."""
import pickle
import numpy as np
from .recipes import get_unique_ingredients, get_unique_cuisines, get_unique_diets
from numpy import dot
from numpy.linalg import norm
import heapq
from random import shuffle
import collections
from django.conf import settings
import os

def load_features_vocabs():
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'features_vocab.pkl'),'rb') as f:
        vocab = pickle.load(f)
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'features_vocab_inv.pkl'),'rb') as f:
        vocab_inv = pickle.load(f)
    return vocab, vocab_inv

def create_features_vocab(incl_diets = False):
    """ Create the set of features that will be used to build user/recipes profiles."""
    ingredients = get_unique_ingredients()
    cuisines = get_unique_cuisines()
    features = ingredients + cuisines
    if incl_diets:
        features += get_unique_diets()
    vocab = {}
    for i, element in enumerate(features):
        if element != "": vocab[i] = element
    return vocab, {val: key for key,val in vocab.items()}

def load_unique_ingredients():
    """ Load mapping from ingredient_name to ingredient_id."""
    with open('../sample_data/ingredients.pkl','rb') as f:
        vocab = pickle.load(f)
    return vocab


def compute_daily_calories_intake(user):
    """ Based on user current bmi and goal bmi, return daily required calories."""
    # current_bmi = 703* user['weight'] / (user['height']*12)**2
    return 1800

def create_recipes_profiles(recipes, features_vocab_inv, incl_diets = False):
    """Create vector models for recipes."""
    recipes_models = {}
    for id,recipe in recipes.items():
        vec_model = np.zeros((1, len(features_vocab_inv)))
        features = recipe.ingredients + recipe.cuisines
        if incl_diets: features += recipe.diets
        for feature_name in features:
            if feature_name in features_vocab_inv:
                vec_model[0,features_vocab_inv[feature_name]] = 1
        recipes_models[id] = vec_model
    return recipes_models

def create_user_profile(user_recipes, features_vocab_inv, incl_diets = False):
    """
    Given a list of recipes for a user, construct a user profile.
    :param user_recipes: a dict of recipe id to recipe object
    :param features_vocab_inv: dict of feature name to feature index
    :return:
    """
    vec_model = np.zeros((1, len(features_vocab_inv)))
    for recipe in user_recipes.values():
        #ingredients
        features = recipe.ingredients + recipe.cuisines
        if incl_diets: features += recipe.diets
        for feature_name in features:
            if feature_name in features_vocab_inv:
                vec_model[0,features_vocab_inv[feature_name]]+=1

    vec_model/=np.max(vec_model, axis = 1)
    return vec_model

def cosine_similarity(a, b):
    cos_sim = dot(a, b.T) / (norm(a) * norm(b))
    return cos_sim[0]

def find_k_most_similar_recipes(user_profile, rec_ids_to_profiles, count = 10):
    """
    Compute the most similar recipes to the user profile.
    :param user_profile: user vector space model.
    :param rec_ids_to_profiles: map of recipe id to recipe vector space model.
    :return:
    """
    if count > len(rec_ids_to_profiles):
        return [t[0] for t in rec_ids_to_profiles]
    heap = []
    for rec_id,recipe in rec_ids_to_profiles:
        if len(heap) < count:
            heapq.heappush(heap, (-cosine_similarity(recipe, user_profile),rec_id))
        else:
            heapq.heappushpop(heap, (-cosine_similarity(recipe, user_profile), rec_id))
    return [h[1] for h in heap]

def create_weekly_recommendations(meal_type_to_recipes, rec_ids_to_recipe, recipes_to_dict = False):
    week_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    for val in meal_type_to_recipes.values():
        shuffle(val)
    weekly_plan = collections.defaultdict(dict)
    for i,day in enumerate(week_days):
        for meal_type, recipes in meal_type_to_recipes.items():
            if recipes_to_dict: weekly_plan[day][meal_type] = rec_ids_to_recipe[recipes[i]]._asdict()
            else: weekly_plan[day][meal_type] = rec_ids_to_recipe[recipes[i]]
    return weekly_plan

def get_toy_user():
    return {'id':1, 'name': 'Efi', 'weight': 130.073, 'height': 5.24934, 'bmigoal': None, 'gender': 'Female', 'age': 28}
