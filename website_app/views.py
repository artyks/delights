from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Purchase, MenuItem, Ingredient, RecipeRequirement
from .business_services import calculate_revenue, calculate_costs, recalculate_inventory_left

@login_required
def home(request):
    revenue_week = calculate_revenue(purchase_model = Purchase, period_in_days = 7)
    costs_week = calculate_costs(purchase_model= Purchase, period_in_days = 7)
    context = {
        "revenue_week" : revenue_week,
        "costs_week" : costs_week,
        "profit_week" : revenue_week - costs_week,
    }
    return render(request, "website_app/home.html", context)


# List views:
class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "website_app/purchases.html"

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "website_app/menu_items.html"

class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "website_app/inventory.html"


# Create views:
class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "website_app/add_purchase.html"
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            menu_item_cleaned = form.cleaned_data['menu_item']
            recalculate_inventory_left(menu_items=menu_item_cleaned, ingredient_model=Ingredient)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "website_app/add_menu_item.html"
    fields = ["name", "price",]

class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "website_app/add_ingredients_to_menu_i.html"
    fields = ["ingredient", "amount_needed"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.active_menu_item = self.model.menu_item.get_queryset().get(id=self.kwargs["menu_pk"])
        return context
    def get_success_url(self) -> str:
        return  reverse_lazy("menu_item_details", kwargs={"pk" : self.kwargs["menu_pk"]})
    
    def form_valid(self, form):
        form.instance.menu_item = self.model.menu_item.get_queryset().get(id=self.kwargs["menu_pk"])
        return super().form_valid(form)


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "website_app/add_ingredient.html"
    fields = "__all__"



# Update views:
class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Purchase
    template_name = "website_app/update_purchase.html"
    fields = "__all__"
    def get_success_url(self) -> str:
        if self.kwargs["detail_success"] == "True":
            return  reverse_lazy("purchase_details", kwargs={"pk" : self.kwargs["pk"]})
        else:
            return super().get_success_url()

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "website_app/update_menu_item.html"
    fields = ["name", "price",]
    def get_success_url(self) -> str:
        if self.kwargs["detail_success"] == "True":
            return  reverse_lazy("menu_item_details", kwargs={"pk" : self.kwargs["pk"]})
        else:
            return super().get_success_url()

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "website_app/update_ingredient.html"
    fields = "__all__"


# Delete views:
class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "website_app/delete_purchase.html"
    success_url = reverse_lazy('purchases')

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "website_app/delete_menu_item.html"
    success_url = reverse_lazy('menu_items')

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "website_app/delete_ingredient.html"
    success_url = reverse_lazy('ingredients')


# Details views:
class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = Purchase
    template_name = "website_app/purchase_details.html"

class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = "website_app/menu_item_details.html"


