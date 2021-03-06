from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """ Seriazlier for tag objects"""

    class Meta:
        model  = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient object"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe object"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'price', 'time_minutes', 'tags', 'ingredients', 'link')
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail object"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
