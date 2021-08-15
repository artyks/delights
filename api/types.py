import graphene
from website_app.models import Purchase, MenuItem, RecipeRequirement, Ingredient
from graphene_django import DjangoObjectType, DjangoListField


class PurchaseType(DjangoObjectType):
    class Meta:
        model = Purchase
        fields = ("id", "time_stamp", "menu_item")

    total = graphene.Float()

    def resolve_total(root, info):
        return root.get_total()


class MenuItemType(DjangoObjectType):
    class Meta:
        model = MenuItem
        fields = ("id", "name", "price", "ingredients", "recipe_requirements")


class RecipeRequirementType(DjangoObjectType):
    class Meta:
        model = RecipeRequirement
        fields = ("menu_item", "ingredient", "amount_needed")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "amount_left", "per_unit_measure", "price_per_unit")