from rest_framework import serializers

from recipes.serializers import RecipeSimpleSerializer
from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор Подписок"""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user

        return (user.is_authenticated
                and user.authors.filter(author=obj.author.id).exists())

    def get_recipes_count(self, obj):

        return obj.author.recipes.count()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        recipes = obj.author.recipes.all()

        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]

        return RecipeSimpleSerializer(recipes, many=True).data

    def validate(self, data):
        request = self.context['request']
        user = request.user
        author_id = data['author'].id

        if user == author_id:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя.'
            )

        if Subscription.objects.filter(user=user, author=author_id).exists():
            raise serializers.ValidationError('Вы уже подписаны на автора.')

        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        author = validated_data['author']

        subscription = Subscription(user=user, author=author)
        subscription.save()

        return subscription

    def destroy(self, instance):
        instance.delete()
