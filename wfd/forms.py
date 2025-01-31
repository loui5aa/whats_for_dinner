from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, MealPlanItem

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'method', 'tags']

class MealPlanItemForm(forms.ModelForm):
    class Meta:
        model = MealPlanItem
        fields = ['day', 'recipe']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) #Gets logged in user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['recipe'].queryset = Recipe.objects.filter(user=user) #Shows only users recipes