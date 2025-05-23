# Generated by Django 4.0.2 on 2025-05-01 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0002_alter_recipeingredient_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.recipe'),
        ),
    ]
