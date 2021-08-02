from datetime import datetime, timedelta

# .models functions

    # Purchase
def get_purchase_total(menu_items):
    total = 0
    for menu_item in menu_items.all():
        total += menu_item.price
    return round(total, 1)

def get_purchase_cost(menu_items):
    cost = 0
    for menu_item in menu_items.all():
        cost += menu_item.get_cost()
    return round(cost, 1)

    # MenuItem
def get_menu_item_ingredients(menu_item_id, recipe_requirements):
    ingredients_dict = {}
    for req in recipe_requirements.filter(menu_item=menu_item_id):
        ingredient = ingredients_dict[req.ingredient.id] = {}
        ingredient["name"] = req.ingredient.name
        ingredient["amount_needed"] = req.amount_needed
        ingredient["unit"] = req.ingredient.per_unit_measure
        ingredient["price_per_unit"] = req.ingredient.price_per_unit
        ingredient["cost"] = req.ingredient.price_per_unit * req.amount_needed
        ingredient["amount_left"] = req.ingredient.amount_left
    return ingredients_dict

# def get_menu_item_ingredients(menu_item_id, recipe_requirements):
#     ingredients = []
#     i = 0
#     for req in recipe_requirements.filter(menu_item=menu_item_id):
#         ingredient = {}
#         ingredient["id"] = req.ingredient.id
#         ingredient["name"] = req.ingredient.name
#         ingredient["amount_needed"] = req.amount_needed
#         ingredient["unit"] = req.ingredient.per_unit_measure
#         ingredient["price_per_unit"] = req.ingredient.price_per_unit
#         ingredient["cost"] = req.ingredient.price_per_unit * req.amount_needed
#         ingredient["amount_left"] = req.ingredient.amount_left
#         ingredients.append(ingredient)
#         i += 1
#     return ingredients

def get_menu_item_cost(ingredients):
    cost = 0
    for ingredient in ingredients.values():
        cost += ingredient["cost"]
    return cost



# .views functions

    # 'home' view. Calculates revenue for Purchases made in last 'period_in_days' days.
def calculate_revenue(purchase_model, period_in_days):
    revenue = 0
    for purchase in purchase_model.objects.filter(time_stamp__date__gte=(datetime.now() - timedelta(days=period_in_days))):
        revenue += purchase.get_total()
    return revenue

    # 'home' view. Calculate costs for Purchases made in last 'period_in_days' days.
def calculate_costs(purchase_model, period_in_days):
        costs = 0
        for purchase in purchase_model.objects.filter(time_stamp__date__gte=(datetime.now() - timedelta(days=period_in_days))):
            for menu_item in purchase.menu_item.all():
                costs += menu_item.get_cost()
        return costs

    # 'PurchaseCreateView' view. Recalculates inventory balances.
def recalculate_inventory_left(menu_items, ingredient_model):
    for menu_item in menu_items:
        for id, ingredient in menu_item.get_ingredients().items():
            ingredient_instance = ingredient_model.objects.get(pk=id)
            ingredient_instance.amount_left -= ingredient["amount_needed"]
            ingredient_instance.save()
            
