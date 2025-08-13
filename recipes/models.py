from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(TimeStamped):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Ingredient(TimeStamped):
    name = models.CharField(max_length=64, unique=True)
    def __str__(self): return self.name

class Recipe(TimeStamped):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    steps = models.TextField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self): return self.title

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'slug': self.slug})

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])
    unit = models.CharField(max_length=16, default='g')
    class Meta:
        unique_together = ('recipe', 'ingredient')

class Comment(TimeStamped):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)

class Favorite(TimeStamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')
    class Meta:
        unique_together = ('user', 'recipe')

class Collection(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('owner', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.owner})"

class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='in_collections')

    class Meta:
        unique_together = ('collection', 'recipe')
        ordering = ['recipe__title']

    def __str__(self):
        return f"{self.collection.name} -> {self.recipe.title}"