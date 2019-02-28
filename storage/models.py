from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)

class Locations(models.Model):
	user_id = models.CharField(max_length=200, primary_key=True)
	longitude = models.FloatField()
	latitude = models.FloatField()
	timestamp = models.PositiveIntegerField()

class StepCount(models.Model):
	user_id = models.CharField(max_length=200, primary_key=True)
	stepCount = models.PositiveIntegerField()
	timestamp = models.PositiveIntegerField()
