from django.urls import path
from .views import RecipeListAPI, RecipeDetailAPI

app_name = "api"

urlpatterns = [
    path("recipes/", RecipeListAPI.as_view(), name="recipe-list"),
    path("recipes/<slug:slug>/", RecipeDetailAPI.as_view(), name="recipe-detail"),
]
