from .recipes import RecipeAPIRetriever

def create_user_recipes(number=20):
    retriever = RecipeAPIRetriever()
    return retriever.retrieve_random_recipes(number=10)

def collect_toy_data_by_calories(count = 1):
    retriever = RecipeAPIRetriever()
    daily_meal_plans, recipes = retriever.retrieve_recipe_data(calories=2000, count=count)
    return daily_meal_plans, recipes


def collect_toy_data_to_show_to_user():
    retriever = RecipeAPIRetriever()
    return retriever.retrieve_random_recipes(number = 10)