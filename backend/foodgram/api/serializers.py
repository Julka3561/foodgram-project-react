import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer to work with custom User creation model."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    """Serializer to work with custom User model."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.follower.filter(author=obj.id).exists()
        return False


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer to work with Ingredient model."""
    class Meta:
        model = Ingredient
        fields = ('__all__')  # TODO проверки на уникальность из бд


class TagSerializer(serializers.ModelSerializer):
    """Serializer to work with Tag model."""
    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, value):  # TODO настроить валидацию по требованию ревьювера
        if value <= 0:
            raise serializers.ValidationError(
                'Количество не может быть меньше 1.')
        return value


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer to work with Recipe list/retrieve."""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='recipe_ingredients')
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.favorite.filter(recipe=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.cart.filter(recipe=obj.id).exists()
        return False


class RecipeCreateSerializer(RecipeSerializer):
    """Serializer to work with Recipe create."""
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть менее минуты.')
        return value

    def save_ingredients(self, recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient['amount']
            ingredients_list.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=current_amount))
        IngredientRecipe.objects.bulk_create(
                ingredients_list)

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.save_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        instance.ingredients.clear()
        recipe = instance
        self.save_ingredients(recipe, ingredients)
        instance.save()
        return instance


class MiniRecipeSerializer(RecipeSerializer):
    """Serializer to work with MiniRecipe."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscriptionSerializer(CustomUserSerializer):
    """Serializer to work with Subscription model."""
    recipes = MiniRecipeSerializer(read_only=True, many=True)
    recipes_count = serializers.IntegerField(source='recipes.count',
                                             read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
