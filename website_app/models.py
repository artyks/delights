from django.db import models
from django.db.models.base import Model
from django.urls import reverse_lazy, reverse
from .business_services import get_purchase_total, get_menu_item_ingredients, get_menu_item_cost, get_purchase_cost

# Create your models here.
class Purchase(models.Model):
   
    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("purchases")

    # Custom methods:

    def get_total(self):
         return get_purchase_total(self.menu_item)
         
    def get_costs(self):
        return get_purchase_cost(menu_items = self.menu_item)

    def get_menu_items_amount(self):
        return len(self.menu_item.all())

    time_stamp = models.DateTimeField(auto_now_add=True)
    menu_item = models.ManyToManyField(
        "MenuItem", 
        related_name="purchases",
    )
    total = get_total
    

class MenuItem(models.Model):

    class Meta:
        verbose_name = "MenuItem"
        verbose_name_plural = "MenuItems"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("menu_items")

    def get_ingredients(self):
        return get_menu_item_ingredients(menu_item_id=self.id, recipe_requirements=self.recipe_requirements)

    def get_cost(self):
        return get_menu_item_cost(ingredients=self.get_ingredients())
    name = models.CharField(max_length=100)
    price = models.FloatField()
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeRequirement",
        related_name="menu_items",
    )


class RecipeRequirement(models.Model):

    menu_item = models.ForeignKey("MenuItem", related_name="recipe_requirements", on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey("Ingredient", related_name="recipe_requirements", on_delete=models.SET_NULL, null=True, blank=False)
    amount_needed = models.IntegerField(default=1)

    class Meta:
        verbose_name = "RecipeRequirement"
        verbose_name_plural = "RecipeRequirements"

    def get_absolute_url(self):
        return reverse("menu_items")


class Ingredient(models.Model):

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ingredients")

    name = models.CharField(max_length=100)
    amount_left = models.IntegerField()

    GRAMS = "gr."
    PIECES = "pc."
    EGGS = "egg"
    MILLILITRES = "ml."
    OUNCES = "oz."

    PER_UNIT_MEASURES = [
        (PIECES, "Pieces"),
        (GRAMS, "Grams"),
        (EGGS, "Eggs"),
        (MILLILITRES, "Millilitres"),
        (OUNCES, "Ounces"),
    ]

    per_unit_measure = models.CharField(
        choices=PER_UNIT_MEASURES,
        default=GRAMS,
        max_length=50,
        )
    price_per_unit = models.FloatField()
    