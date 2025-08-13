# recipes/forms.py
from django import forms
from .models import Recipe, Comment, Collection, CollectionItem

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'slug', 'category', 'description', 'steps', 'is_published']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишете коментар...'}),
        }

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']

class AddRecipeToCollectionForm(forms.Form):
    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.filter(is_published=True),
        label='Рецепта'
    )