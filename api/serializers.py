from rest_framework import serializers
from recipes.models import Recipe, Category, Collection, CollectionItem


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


class CollectionItemSerializer(serializers.ModelSerializer):
    recipe_title = serializers.CharField(source="recipe.title", read_only=True)
    recipe_slug = serializers.SlugField(source="recipe.slug", read_only=True)

    class Meta:
        model = CollectionItem
        fields = ("id", "recipe", "recipe_title", "recipe_slug")


class CollectionListSerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField(source="items.count", read_only=True)

    class Meta:
        model = Collection
        fields = ("id", "name", "description", "items_count", "owner")
        read_only_fields = ("owner",)


class CollectionDetailSerializer(serializers.ModelSerializer):
    items = CollectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ("id", "name", "description", "items", "owner")
        read_only_fields = ("owner",)
