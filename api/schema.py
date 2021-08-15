import graphene
from graphene.types.objecttype import ObjectType
from graphene_django import DjangoObjectType, DjangoListField

from website_app.models import Purchase, MenuItem, Ingredient, RecipeRequirement
from .types import IngredientType, PurchaseType, MenuItemType

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    all_purchases = graphene.List(PurchaseType)
    all_menu_items = DjangoListField(MenuItemType)

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.all()

    def resolve_all_purchases(root, info):
        return Purchase.objects.all()

    def resolve_all_menu_items(root, info):
        return MenuItem.objects.all()

    ingredient_by_id = graphene.Field(IngredientType, id=graphene.String())
    purchase_by_id = graphene.Field(PurchaseType, id=graphene.String())

    def resolve_ingredient_by_id(root, info, id):
        return Ingredient.objects.get(pk=id)

    def resolve_purchase_by_id(root, info, id):
        return Purchase.objects.get(pk=id)

class Mutation(graphene.ObjectType):
    pass

