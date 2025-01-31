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


