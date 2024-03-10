<<<<<<< HEAD
<<<<<<< HEAD
import api.serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from djoser.serializers import UserCreateSerializer as BaseUserRegistration
from djoser.serializers import UserSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe

from .models import Follow, User
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from .models import User, Follow

from django.core import exceptions
from recipes.models import Recipe
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password

from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import api.serializers
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3


class UserSerializer(UserSerializer):
    """Профиль пользователя"""

    is_subscribed = serializers.SerializerMethodField()
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
<<<<<<< HEAD
<<<<<<< HEAD
        if (
            self.context.get('request')
            and not self.context['request'].user.is_anonymous
        ):
            return Follow.objects.filter(
                follower=self.context['request'].user,
                following=obj
            ).exists()
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        if (self.context.get('request')
            and not self.context['request'].user.is_anonymous):
            return Follow.objects.filter(
                follower=self.context['request'].user,
                following=obj
                ).exists()
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


<<<<<<< HEAD
<<<<<<< HEAD
class UserCreateSerializer(BaseUserRegistration):
    """Регистрация пользователя"""

    class Meta(BaseUserRegistration.Meta):

=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
class UserCreateSerializer(UserCreateSerializer):
    """Регистрация пользователя"""

    class Meta:
        model = User
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'password',)

    def validate_username(self, data):
        invalid_name = ['me', 'set_password']
        name = self.initial_data.get('username')
        if name in invalid_name:
            raise ValidationError(
                f'Использовать "{name}" нельзя. Выберите другое имя!'
<<<<<<< HEAD
<<<<<<< HEAD
            )
=======
                )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        return data


class PasswordChangeSerializer(serializers.ModelSerializer):
    """Изменение пароля"""

    new_password = serializers.CharField(required=True)
<<<<<<< HEAD
<<<<<<< HEAD
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password',)
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    current_password = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('new_password', 'current_password',)
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

    def update(self, instance, validated_data):

        request = self.context['request']
        user_password = request.user.password
<<<<<<< HEAD
<<<<<<< HEAD
        if not check_password(
            validated_data['current_password'], user_password
        ):
=======
        if not check_password(validated_data['current_password'], user_password):
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
        if not check_password(validated_data['current_password'], user_password):
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
            raise ValidationError(
                {'current_password': 'Неправильный текущий пароль!'}
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего!'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data

    def validate(self, obj):
        try:
            validate_password(obj['new_password'])
        except exceptions.ValidationError as err:
            raise ValidationError(
                {'new_password': list(err.messages)}
<<<<<<< HEAD
<<<<<<< HEAD
            )
=======
                )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        return super().validate(obj)


class FollowSerializer(serializers.ModelSerializer):
    """Подписка пользователя, проверка входных данных"""
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.following)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return api.serializers.RecipeSerializer(recipes, many=True).data
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    def get_is_subscribed(self, obj):
        follower = self.context.get('request').user
        if not follower.is_anonymous:
            return Follow.objects.filter(
                follower=obj.following,
                following=obj.follower).exists()
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()

    def validate(self, data):
        following = self.context.get('following')
        follower = self.context.get('request').user
        if Follow.objects.filter(
                following=following,
                follower=follower).exists():
            raise ValidationError(
<<<<<<< HEAD
<<<<<<< HEAD
                {'errors': 'Вы уже подписаны на этого пользователя!'},
                code=status.HTTP_400_BAD_REQUEST
            )
=======
               {'errors': 'Вы уже подписаны на этого пользователя!'},
                code=status.HTTP_400_BAD_REQUEST)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
               {'errors': 'Вы уже подписаны на этого пользователя!'},
                code=status.HTTP_400_BAD_REQUEST)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        if follower == following:
            raise ValidationError(
                {'errors': 'Вы не можете подписаться на себя!'},
                code=status.HTTP_400_BAD_REQUEST)
        return data
