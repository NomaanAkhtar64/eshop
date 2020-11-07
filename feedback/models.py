from django.db import models

# Create your models here.
class Review(models.Model):
    rating = models.FloatField()
    message = models.TextField()
    recommendations = models.PositiveIntegerField(default=0)
    un_recommendations = models.PositiveIntegerField(default=0)