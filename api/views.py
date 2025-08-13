from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe, Collection, CollectionItem
from .serializers import (
    RecipeListSerializer, RecipeDetailSerializer,
    CollectionListSerializer, CollectionDetailSerializer, CollectionItemSerializer,
)
from .permissions import IsOwner



class RecipeListAPI(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_published=True).select_related("category", "owner").order_by("-created_at")
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.AllowAny]


class RecipeDetailAPI(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(is_published=True).select_related("category", "owner")
    serializer_class = RecipeDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"



class CollectionListCreateAPI(generics.ListCreateAPIView):
    """
    GET: списък с колекциите на текущия потребител
    POST: създаване на колекция (owner = request.user)
    """
    serializer_class = CollectionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user).order_by("name")

    def perform_create(self, serializer):
        name = serializer.validated_data.get("name", "").strip()
        if Collection.objects.filter(owner=self.request.user, name=name).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"name": "Вече имате колекция с това име."})
        serializer.save(owner=self.request.user)


class CollectionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/PATCH/DELETE за конкретна колекция (само owner)
    """
    serializer_class = CollectionDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Collection.objects.all()

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class CollectionAddItemAPI(APIView):
    """
    POST: добавя Recipe към Collection.
    Body: {"recipe": <recipe_id>}
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request, pk):
        try:
            collection = Collection.objects.get(pk=pk)
        except Collection.DoesNotExist:
            return Response({"detail": "Не е намерена колекция."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, collection)

        recipe_id = request.data.get("recipe")
        if not recipe_id:
            return Response({"recipe": "Изисква се id на рецепта."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(pk=recipe_id, is_published=True)
        except Recipe.DoesNotExist:
            return Response({"recipe": "Невалидна или непубликувана рецепта."}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CollectionItem.objects.get_or_create(collection=collection, recipe=recipe)
        ser = CollectionItemSerializer(item)
        return Response(ser.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CollectionRemoveItemAPI(APIView):
    """
    DELETE: премахва CollectionItem от колекцията.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def delete(self, request, pk, item_id):
        try:
            collection = Collection.objects.get(pk=pk)
        except Collection.DoesNotExist:
            return Response({"detail": "Не е намерена колекция."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, collection)

        try:
            item = CollectionItem.objects.get(pk=item_id, collection=collection)
        except CollectionItem.DoesNotExist:
            return Response({"detail": "Елементът не е намерен."}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
