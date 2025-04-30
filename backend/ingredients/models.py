from django.db import models


class Ingredient(models.Model):
    name = models.CharField(null=False, max_length=200)
    measurement_unit = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name
