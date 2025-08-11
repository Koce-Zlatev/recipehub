from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Comment, Favorite

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'owner__username')
    ordering = ('-created_at',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [RecipeIngredientInline]

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Comment)
admin.site.register(Favorite)
