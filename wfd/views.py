from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from .forms import CustomUserCreationForm, NewRecipeForm, MealPlanItemForm
from .models import Recipe,MealPlan, MealPlanItem, ShoppingList
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("Hello, World!")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() #Saves new user
            messages.success(request, 'Account created successfully. You can now log in!')
            return redirect('login') #Redirects to login
    else:
        form= CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = NewRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect ('recipe_list')
    else:
        form = NewRecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form' : form})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.user != request.user:
        return HttpResponseForbidden("You do not have permission to delete this recipe.")
    
    if request.method == "POST":
        recipe.delete()
        return redirect('recipe_list')
    
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})

@login_required
def meal_plan_view(request):
    meal_plan, created = MealPlan.objects.get_or_create(user=request.user)  # Get or create a meal plan for the user
    items = meal_plan.items.all()

    if request.method == 'POST':
        form = MealPlanItemForm(request.POST, user=request.user)
        if form.is_valid():
            meal_item = form.save(commit=False)
            meal_item.meal_plan = meal_plan
            meal_item.save()
            return redirect('meal_plan')
        
    else:
        form = MealPlanItemForm(user=request.user)
    return render(request, 'meal_plan.html', {'meal_plan': meal_plan, 'items': items, 'form': form})

@login_required
def generate_shopping_list(request):
    meal_plan = MealPlan.objects.filter(user=request.user).first()
    if not meal_plan:
        return redirect('meal_plan')

    ingredient_list = []
    for item in meal_plan.items.all():
        recipe = item.recipe
        ingredient_list.extend(recipe.ingredients.split("\n"))
    shopping_items = {}
    for ingredient in ingredient_list:
        ingredient = ingredient.strip()
        if ingredient:
            shopping_items[ingredient] = shopping_items.get(ingredient, 0) + 1
    
    shopping_list, created = ShoppingList.objects.get_or_create(user=request.user)
    shopping_list.items = "\n".join([f"{v}x {k}" for k, v in shopping_items.items()])
    shopping_list.save()

    return render(request, 'shopping_list.html', {'shopping_list': shopping_list})
