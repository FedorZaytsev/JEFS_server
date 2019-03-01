from django.urls import path, include
from .views import *


urlpatterns = [
    path('storage/stepcount', StepCountView.as_view()),
    path('storage/location', LocationView.as_view()),
    path('recommendations/workouts', WorkoutRecommendation.as_view()),
    path('recommendations/recepies', RecepiesRecommendation.as_view()),
    path('', UserView.as_view())
]
