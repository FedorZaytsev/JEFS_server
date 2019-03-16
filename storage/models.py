from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    weight = models.FloatField()
    height = models.FloatField()
    bmigoal = models.FloatField()
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    cuisine = models.CharField(max_length=2000)
    targetWeight = models.FloatField()


class Locations(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	longitude = models.FloatField()
	latitude = models.FloatField()
	timestamp = models.PositiveIntegerField()

	def __str__(self):
		return str({
			'longitude': self.longitude,
			'latitude': self.latitude,
			'timestamp': self.timestamp,
		})

class StepCount(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	stepCount = models.PositiveIntegerField()
	timestamp = models.PositiveIntegerField()

	def __str__(self):
		return str({
			'stepCount': self.stepCount,
			'timestamp': self.timestamp,
		})

class Recipe(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=200)
	cuisines = models.CharField(max_length=500)
	vegan = models.BooleanField()
	image = models.CharField(max_length=200)
	vegetarian = models.BooleanField()
	ingredients = models.CharField(max_length=1000)
	glutenFree = models.BooleanField()
	calories = models.PositiveIntegerField()
	fat = models.PositiveIntegerField()
	carb = models.PositiveIntegerField()
	protein = models.PositiveIntegerField()


class LikedRecepy(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	timestamp = models.DateField()	

class UserHistory(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	weight = models.FloatField()
	height = models.FloatField()
	timestamp = models.DateField()

