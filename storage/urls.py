from django.urls import path, include
from .views import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

urlpatterns = [
    path('storage/stepcount', StepCountView.as_view()),
    path('storage/location', LocationView.as_view()),
    path('', UserView.as_view())
]
