from django.urls import path
from .views import (
    RecipeListAPI, RecipeDetailAPI,
    CollectionListCreateAPI, CollectionDetailAPI,
    CollectionAddItemAPI, CollectionRemoveItemAPI,
)

app_name = "api"

urlpatterns = [
    path("recipes/", RecipeListAPI.as_view(), name="recipe-list"),
    path("recipes/<slug:slug>/", RecipeDetailAPI.as_view(), name="recipe-detail"),

    path("collections/", CollectionListCreateAPI.as_view(), name="collection-list"),
    path("collections/<int:pk>/", CollectionDetailAPI.as_view(), name="collection-detail"),
    path("collections/<int:pk>/add/", CollectionAddItemAPI.as_view(), name="collection-add-item"),
    path("collections/<int:pk>/remove/<int:item_id>/", CollectionRemoveItemAPI.as_view(), name="collection-remove-item"),
]
