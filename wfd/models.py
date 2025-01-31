from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    CATEGORY_CHOICES = [ 
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
    ]

    title = models.CharField(max_length = 255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField(help_text = "Enter each ingredient on a new line.")
    method= models.TextField()
    tags = models.CharField(max_length=20, choices= CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meal Plan for {self.user.username} - {self.created_at.date()}"

class MealPlanItem(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="items")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.recipe.title} on {self.day}"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.TextField()  # Will store combined ingredients as text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shopping List for {self.user.username} - {self.created_at.date()}"
