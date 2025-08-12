from rest_framework import generics, permissions
from recipes.models import Recipe
from .serializers import RecipeListSerializer, RecipeDetailSerializer

class RecipeListAPI(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_published=True).select_related("category", "owner").order_by("-created_at")
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.AllowAny]

class RecipeDetailAPI(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(is_published=True).select_related("category", "owner")
    serializer_class = RecipeDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"