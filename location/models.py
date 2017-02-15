from __future__ import unicode_literals

from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.country_name


class  State(models.Model):
    country = models.ForeignKey(Country)
    state_name  = models.CharField(max_length = 100)

    def __str__(self):
        return self.state_name

class City(models.Model) :
    #state = models.ForeignKey(State)
    city_name  = models.CharField(max_length = 100)
    corrected_city_name=models.CharField(max_length=100)

    def __str__(self):
        return self.city_name

class CorrectedCity(models.Model) :
    city_name=models.CharField(max_length=100)

    def __str__(self):
        return self.city_name        
