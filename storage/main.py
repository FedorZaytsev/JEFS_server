""" I used this module to create toy data and text the recommendations."""
from storage.create_toy_data import *
from storage.recommend_helper import create_features_vocab
from storage.recommendations import recommend_recipes, get_random_recipe_data
import pickle
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server225.settings')
from django.conf import settings

def create_toy_data():
    meal_plans, recipes = collect_toy_data_by_calories(count = 10)
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'by_calories_retrieval/daily_meal_plans.json'), 'w') as f:
        f.write(json.dumps(meal_plans, sort_keys=True, indent=4))
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'by_calories_retrieval/recipes_infos.pkl'), 'wb') as f:
        pickle.dump(recipes,f)

    random_recipes = collect_toy_data_to_show_to_user()
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'to_show_to_the_user/random_recipes.pkl'), 'wb') as f:
        pickle.dump(random_recipes, f)

    user_recipes = create_user_recipes(number = 20)
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'user_ingreds_1.pkl'), 'wb') as f:
        pickle.dump(user_recipes, f)

    vocab, inv_vocab = create_features_vocab()
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'features_vocab.pkl'), 'wb') as f:
        pickle.dump(vocab, f)
    with open(os.path.join(settings.TOY_DATA_FOLDER, 'features_vocab_inv.pkl'), 'wb') as f:
        pickle.dump(inv_vocab, f)
    pass

if __name__=='__main__':
    # create_toy_data()
    # most_similar_per_meal_type = recommend_recipes(userId=1)
    # print(most_similar_per_meal_type)
    recipes = get_random_recipe_data(3, use_toy_data=True, to_json=True)
    print(recipes)