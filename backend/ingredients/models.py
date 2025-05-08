from django.db import models

from foodgram.constants import (
    INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
    INGREDIENT_NAME_MAX_LENGTH,
)


class Ingredient(models.Model):
    name = models.CharField(
        null=False,
        max_length=INGREDIENT_NAME_MAX_LENGTH,
    )
    measurement_unit = models.CharField(
        null=False,
        max_length=INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
