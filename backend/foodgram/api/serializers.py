from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
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
            user = User.objects.get(username=self.context['request'].user)
            return user.follower.filter(author=obj.id).exists()
        return False


class SubscriptionSerializer(CustomUserSerializer):
    """Serializer to work with Subscriptions model."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

# TODO добавить поля recipes и recipes_count
