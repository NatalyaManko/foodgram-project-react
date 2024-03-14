import api.serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistration
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe

from .models import Follow, User


class UserSerializer(UserSerializer):
    """Профиль пользователя"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        if (
            self.context.get('request')
            and not self.context['request'].user.is_anonymous
        ):
            return Follow.objects.filter(
                follower=self.context['request'].user,
                following=obj
            ).exists()
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserCreateSerializer(BaseUserRegistration):
    """Регистрация пользователя"""

    class Meta:
        model = User

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
            )
        return data


class FollowSerializer(serializers.ModelSerializer):
    """Подписка пользователя"""

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

    def validate(self, data):
        following = self.context.get('following')
        follower = self.context.get('request').user
        if follower == following:
            raise ValidationError(
                {'errors': 'Вы не можете подписаться на себя!'},
            )
        if Follow.objects.filter(
                following=following,
                follower=follower).exists():
            raise ValidationError(
                {'errors': 'Вы уже подписаны на этого пользователя!'},
            )
        super().validate(data)
        return data

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise ValidationError(
                'Вы не можете подписаться на себя!')
        return value

    def get_is_subscribed(self, obj):
        follower = self.context.get('request').user
        if not follower.is_anonymous:
            return Follow.objects.filter(
                follower=obj.following,
                following=obj.follower).exists()
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.following)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return api.serializers.RecipeSerializer(recipes, many=True).data
