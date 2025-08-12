from rest_framework import serializers
from recipes.models import Recipe, Category

class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")

class RecipeListSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer(read_only=True)
    owner = serializers.CharField(source="owner.username", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:recipe-detail", lookup_field="slug")

    class Meta:
        model = Recipe
        fields = ("title", "slug", "owner", "category", "is_published", "created_at", "url")

class RecipeDetailSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer(read_only=True)
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Recipe
        fields = ("title", "slug", "owner", "category", "description", "steps", "is_published", "created_at", "updated_at")
