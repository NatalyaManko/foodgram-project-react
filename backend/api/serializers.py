import base64
<<<<<<< HEAD
<<<<<<< HEAD

import webcolors
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from rest_framework import exceptions, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            ShoppingCart,
                            Tag)
from users.serializers import UserSerializer

=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

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
<<<<<<< HEAD
<<<<<<< HEAD


=======
    
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тегов"""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


<<<<<<< HEAD
<<<<<<< HEAD
class RecipeTagSerializer(serializers.ModelSerializer):
    """Связная модель с количеством для Рецепта"""
    id = serializers.ReadOnlyField(source='tag.id')
    name = serializers.ReadOnlyField(source='tag.name')
    color = Hex2NameColor(source='tag.color')
    slug = serializers.ReadOnlyField(source='tag.slug')

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Чтение Ингредиентов"""

=======
class IngredientSerializer(serializers.ModelSerializer):
    """Чтение Ингредиентов"""
   
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
class IngredientSerializer(serializers.ModelSerializer):
    """Чтение Ингредиентов"""
   
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
<<<<<<< HEAD
    )

=======
        )
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
        )
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class AddRecipeIngredientSerializer(serializers.ModelSerializer):
    """Ингредиенты с количеством для создания рецепта """

<<<<<<< HEAD
<<<<<<< HEAD
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(
                1, message='Количество ингредиента не может быть меньше 1'
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
   # id =  PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[MinValueValidator(
            1, message='Количество ингредиента не может быть меньше 1'
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
<<<<<<< HEAD
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time',)
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Запись Рецептов"""

<<<<<<< HEAD
<<<<<<< HEAD
    author = UserSerializer(read_only=True)
    ingredients = AddRecipeIngredientSerializer(
        source='recipes_ingredients',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=[
            MinValueValidator(
                1, message='Время приготовления не может быть меньше 1 минуты'
            )
        ]
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

    class Meta:
        model = Recipe
        fields = ('id',
<<<<<<< HEAD
<<<<<<< HEAD
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
=======
                  'tags',                  
                  'author',
                  'ingredients',
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                  'tags',                  
                  'author',
                  'ingredients',
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
                  'image',
                  'name',
                  'text',
                  'cooking_time',
                  )
<<<<<<< HEAD
<<<<<<< HEAD
        read_only_fields = ('author',
                            'is_favorited',
                            'is_in_shopping_cart',)

    def validate(self, data):
        if not data.get('recipes_ingredients', None):
            raise exceptions.ValidationError(
                {'ingredients': 'Поле обязательно для заполнения!'}
            )
        ingredients_arr = []
        for item in data.get('recipes_ingredients'):
            if item in ingredients_arr:
                raise exceptions.ValidationError(
                    'Ингредиент уже выбран!'
                )
            ingredients_arr.append(item)
            if int(item['amount']) < 1:
                raise exceptions.ValidationError(
                    'Количество ингредиента не должно быть меньше 1!'
                )
        if not data.get('tags', None):
            raise exceptions.ValidationError(
                {'tags': 'Поле обязательно для заполнения!'}
            )
        tag_arr = []
        for tag in data.get('tags'):
            if tag in tag_arr:
                raise exceptions.ValidationError(
                    'Теги не должны повторяться!'
                )
            tag_arr.append(tag)
        return data
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

    @staticmethod
    def _save_recipe(recipe, ingredients, tags):
        for ingredient in ingredients:
<<<<<<< HEAD
<<<<<<< HEAD
            amount = ingredient['amount']
            try:
                ingredient = Ingredient.objects.get(
                    id=ingredient['id']
                )
            except ObjectDoesNotExist:
                raise exceptions.ValidationError(
                    {'detail': 'Такой ингредиент не существует!'}
                )
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
            amount = ingredient['amount'] #.amount
#            breakpoint()
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient['id']
            )
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
<<<<<<< HEAD
        instance.tags.set(tags)
=======
    #    instance.tags.set(tags)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    #    instance.tags.set(tags)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        self._save_recipe(instance, ingredients, tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
<<<<<<< HEAD
<<<<<<< HEAD
        display = super().to_representation(instance)
        display['ingredients'] = RecipeIngredientSerializer(
            instance.recipes_ingredients.all(), many=True).data
        display['tags'] = RecipeTagSerializer(
            instance.recipes_tags.all(), many=True).data
        return display

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite.objects.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return ShoppingCart.objects.filter(recipe=obj).exists()
        return False
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        ingredients = super().to_representation(instance)
        ingredients['ingredients'] = RecipeIngredientSerializer(
            instance.recipes_ingredients.all(), many=True).data
        return ingredients
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор чтения Рецептa"""

<<<<<<< HEAD
<<<<<<< HEAD
    author = UserSerializer
    ingredients = RecipeIngredientSerializer(many=True,
                                             read_only=True,
                                             source='recipes_ingredients')
    tags = TagSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField('get_image_url',
                                                  read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    ingredients = RecipeIngredientSerializer(many=True,
                                          read_only=True,
                                          source='recipes_ingredients')
    tags = TagSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField('get_image_url',
                                                  read_only=True)
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
<<<<<<< HEAD
<<<<<<< HEAD
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image_url',
                  'text',
                  'cooking_time',)
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

<<<<<<< HEAD
<<<<<<< HEAD
    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite.objects.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return ShoppingCart.objects.filter(recipe=obj).exists()
        return False


=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор Списка покупок"""
    name = serializers.ReadOnlyField(source='recipe.name',
                                     read_only=True)
    image = Base64ImageField(source='recipe.image',
                             read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
<<<<<<< HEAD
<<<<<<< HEAD
                                            read_only=True)
=======
                                             read_only=True)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                                             read_only=True)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

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
<<<<<<< HEAD
<<<<<<< HEAD
                                            read_only=True)
=======
                                             read_only=True)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                                             read_only=True)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

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
<<<<<<< HEAD
<<<<<<< HEAD
                {'errors': 'Вы уже добавили этот рецепт в избранное!'},
                code=status.HTTP_400_BAD_REQUEST
            )
        return data
=======
               {'errors': 'Вы уже добавили этот рецепт в избранное!'},
                code=status.HTTP_400_BAD_REQUEST
                )
        return data
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
               {'errors': 'Вы уже добавили этот рецепт в избранное!'},
                code=status.HTTP_400_BAD_REQUEST
                )
        return data
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
