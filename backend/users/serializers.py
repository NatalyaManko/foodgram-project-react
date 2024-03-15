from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from subscriptions.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_subscribed', )

    def get_is_subscribed(self, obj):
        if not self.context:
            return False
        user = self.context.get('request').user
        return (user.is_authenticated
                and Subscription.objects.filter(user=user,
                                                author=obj).exists())


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError('Поле должно быть уникальным.')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError('Поле должно быть уникальным.')
        return value

    def validate_password(self, value):
        return make_password(value)


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_current_password(self, value):
        user = self.context['request'].user
        if user.check_password(value):
            return value
        raise serializers.ValidationError('Введён неправильный пароль')

    def validate_new_password(self, value):
        return make_password(value)
