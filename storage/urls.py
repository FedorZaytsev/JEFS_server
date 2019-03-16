from django.urls import path
from .views import *


urlpatterns = [
    path('storage/stepcount', StepCountView.as_view()),
    path('storage/location', LocationView.as_view()),
    path('recommendations/workouts', WorkoutRecommendation.as_view()),
    path('recommendations/recipes', RecepiesRecommendation.as_view()),
    path('storage/recipes', RecipesView.as_view()),
    path('recipe/<int:recipeId>/like', RecipeLikeView.as_view()),
    path('profile', UserProfile.as_view()),
    path('calories', ConsumedCalories.as_view()),
    path('nutrients', ConsumedNutriens.as_view()),
    path('', UserView.as_view())
]
