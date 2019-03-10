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
    ethnicity = models.CharField(max_length=200)


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
	userId = models.ForeignKey(User, on_delete=models.CASCADE,)
	stepCount = models.PositiveIntegerField()
	timestamp = models.PositiveIntegerField()

	def __str__(self):
		return str({
			'stepCount': self.stepCount,
			'timestamp': self.timestamp,
		})

