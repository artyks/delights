import graphene
import api.schema
# from graphene_django import DjangoObjectType

# from website_app.models import Purchase, MenuItem, Ingredient, RecipeRequirement


class Query(
    api.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    api.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, mutation=Mutation)