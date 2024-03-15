import base64

from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr),
                               name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeIngredientSimpleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=settings.MIN_SMALL_NUMBER,
        max_value=settings.MAX_SMALL_NUMBER)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class RecipeSimpleSerializer(serializers.ModelSerializer):
    """Only for subscriptions, favorites and shopping cart display."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredients_in_recipe', read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        if not self.context:
            return False
        user = self.context['request'].user
        return (user.is_authenticated
                and user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        if not self.context:
            return False
        user = self.context['request'].user
        return (user.is_authenticated
                and user.items.filter(recipe=obj).exists())


class RecipeAddChangeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSimpleSerializer(
        source='ingredients_in_recipe', many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    cooking_time = serializers.IntegerField(
        min_value=settings.MIN_SMALL_NUMBER,
        max_value=settings.MAX_SMALL_NUMBER)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'ingredients', 'image',
                  'cooking_time', 'tags', 'author')

    def create_ingredients(self, recipe, ingredients):
        bulk_list = list()
        for ingredient in ingredients:
            bulk_list.append(RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient['amount']))

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data)

        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()

        self.create_ingredients(instance, ingredients)
        instance.tags.set(tags)

        return super().update(instance, validated_data)

    def to_representation(self, value):
        return RecipeSerializer(value).data

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                {'ingredients': 'Пустой список.'})

        unique_ids = set([ingredient['ingredient']['id'].id
                          for ingredient in value])
        if len(value) != len(unique_ids):
            raise serializers.ValidationError(
                {'ingredients': 'Значения должны быть уникальны.'})

        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError({'tags': 'Пустой список.'})

        if len(value) != len(set([tag.id for tag in value])):
            raise serializers.ValidationError(
                {'tags': 'Значения должны быть уникальным.'})

        return value

    def validate(self, obj):
        for field in ('name', 'text', 'cooking_time', 'image',
                      'tags', 'ingredients_in_recipe'):
            if not obj.get(field):
                raise serializers.ValidationError({f'{field}':
                                                   'Поле обязательно.'})

        return obj
