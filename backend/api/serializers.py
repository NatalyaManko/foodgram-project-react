import base64
import webcolors
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from recipes.models import (Ingredient,
                            Recipe,
                            Tag,
                            Favorite,
                            RecipeIngredient,
                            ShoppingCart)
from users.serializers import UserSerializer
from rest_framework.relations import (PrimaryKeyRelatedField)
from django.core.validators import MinValueValidator

from rest_framework import status

class Hex2NameColor(serializers.Field):
    """Сериализатор конвертации кода цвета в hex-формате"""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    """Сериализатор декодирования изображения"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
    
    
class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тегов"""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Чтение Ингредиентов"""
   
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = '__all__',


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Связная модель Ингредиентов с количеством для Рецепта"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
        )
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class AddRecipeIngredientSerializer(serializers.ModelSerializer):
    """Ингредиенты с количеством для создания рецепта """

   # id =  PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[MinValueValidator(
            1, message='Количество ингредиента не может быть меньше 1'
            )
        ]
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов для подписок"""

    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField()
    image = Base64ImageField(
        read_only=True
        )
    cooking_time = serializers.IntegerField()
    
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',                  
                  'image',
                  'cooking_time',
)

 #   def get_image_url(self, obj):
  #      if obj.image:
  #          return obj.image.url
  #      return None


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Запись Рецептов"""

    #id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)
    ingredients = AddRecipeIngredientSerializer(
        source='recipes_ingredients',
        many=True #, write_only=True
        )                                   
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
        )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=[MinValueValidator(
            1, message='Время приготовления не может быть меньше 1 минуты'
            )
        ]
    )

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',                  
                  'author',
                  'ingredients',
                  'image',
                  'name',
                  'text',
                  'cooking_time',
                  )
        read_only_fields = ('author',)

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Добавьте ингредиент!'
                )
        ingredients_arr = []    
        for item in value:
            if item in ingredients_arr:
                raise exceptions.ValidationError(
                    'Ингредиент уже выбран!'
                     )
            ingredients_arr.append(item)
            if int(item['amount']) <= 1:
                raise exceptions.ValidationError(
                    'Количество ингредиента не должно быть меньше 1!'
                    )
        return value
    
    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Выберите хотя бы один тег!'
                )
        tag_arr = []
        for tag in value:
            if tag in tag_arr:
               raise exceptions.ValidationError(
                'Теги не должны повторяться!')
            tag_arr.append(tag)                
        return value

    @staticmethod
    def _save_recipe(recipe, ingredients, tags):
        for ingredient in ingredients:
            amount = ingredient['amount'] #.amount
#            breakpoint()
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient['id']
            )
            RecipeIngredient.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount
            )
        recipe.tags.set(tags)

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        ingredients = validated_data.pop('recipes_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self._save_recipe(recipe, ingredients, tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipes_ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
    #    instance.tags.set(tags)
        self._save_recipe(instance, ingredients, tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        ingredients = super().to_representation(instance)
        ingredients['ingredients'] = RecipeIngredientSerializer(
            instance.recipes_ingredients.all(), many=True).data
        return ingredients


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор чтения Рецептa"""

    ingredients = RecipeIngredientSerializer(many=True,
                                          read_only=True,
                                          source='recipes_ingredients')
    tags = TagSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField('get_image_url',
                                                  read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',                 
                  'ingredients',
 #                 'is_favorited', # находится ли в избранном
                  'is_in_shopping_cart', # находится ли в корзине
                  'name',                  
                  'image_url',
                  'text',
                  'cooking_time',
)
    #    read_only_fields = ('author',)

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор Списка покупок"""
    name = serializers.ReadOnlyField(source='recipe.name',
                                     read_only=True)
    image = Base64ImageField(source='recipe.image',
                             read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                             read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time',)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор Избранного"""
    name = serializers.ReadOnlyField(source='recipe.name',
                                     read_only=True)
    image = Base64ImageField(source='recipe.image',
                             read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                             read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time',)

    def validate(self, data):
        recipe = self.context.get('recipe')
        user = self.context.get('request').user
        if Favorite.objects.filter(
                recipe=recipe,
                user=user).exists():
            raise ValidationError(
               {'errors': 'Вы уже добавили этот рецепт в избранное!'},
                code=status.HTTP_400_BAD_REQUEST
                )
        return data