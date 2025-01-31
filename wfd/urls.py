#wfd/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('meal-plan/', views.meal_plan_view, name='meal_plan'),
    path('shopping-list/', views.generate_shopping_list, name='shopping_list'),
]