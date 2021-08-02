from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # List views:
    path("purchases/", views.PurchaseListView.as_view(), name="purchases"),
    path("menu-items/", views.MenuItemListView.as_view(), name="menu_items"),
    path("inventory/", views.IngredientListView.as_view(), name="ingredients"),
    # Details views:
    path("purchases/<int:pk>/", views.PurchaseDetailView.as_view(), name="purchase_details"),
    path("menu-items/<int:pk>/", views.MenuItemDetailView.as_view(), name="menu_item_details"),
    # Create views:
    path("purchases/add/", views.PurchaseCreateView.as_view(), name="add_purchase"),
    path("menu-items/add/", views.MenuItemCreateView.as_view(), name="add_menu_item"),
    path("inventory/add/", views.IngredientCreateView.as_view(), name="add_ingredient"),
    path("menu_items/<int:menu_pk>/add-ingredient/", views.RecipeRequirementCreateView.as_view(), name="add_ingredient_to_menu_i"),
    # Update views:
    path("purchases/<int:pk>/update/?<str:detail_success>", views.PurchaseUpdateView.as_view(), name="update_purchase"),
    path("menu-items/<int:pk>/update/?<str:detail_success>", views.MenuItemUpdateView.as_view(), name="update_menu_item"),
    path("inventory/<int:pk>/update/", views.IngredientUpdateView.as_view(), name="update_ingredient"),
    # Delete views:
    path("purchases/<int:pk>/delete/", views.PurchaseDeleteView.as_view(), name="delete_purchase"),
    path("menu-items/<int:pk>/delete/", views.MenuItemDeleteView.as_view(),  name="delete_menu_item"),
    path("inventory/<int:pk>/delete/", views.IngredientDeleteView.as_view(), name="delete_ingredient"),
]
