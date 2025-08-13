from django.contrib import admin
from .models import (
    Category, Ingredient, Recipe, RecipeIngredient,
    Comment, Favorite,
    Collection, CollectionItem,
)

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

class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 0

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')
    inlines = [CollectionItemInline]

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Comment)
admin.site.register(Favorite)
