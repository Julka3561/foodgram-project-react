from api.serializers import SubscriptionSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User


class SubscriptionsViewSet(viewsets.GenericViewSet):
    """Custom viewset for users subscribe/unsubscribe and
    list of subscriptions."""
    serializer_class = SubscriptionSerializer
    queryset = User.objects.all()

    @action(detail=False,
            permission_classes=[IsAuthenticated, ],
            )
    def subscriptions(self, request):
        user = self.request.user
        subscriptions = user.follower.all().values('author')
        result = User.objects.filter(id__in=subscriptions)
        page = self.paginate_queryset(result)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated, ])
    def subscription(self, request, pk):
        user = self.request.user
        author = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(author)

        if self.request.method == 'POST':
            subscription = Subscription(user=user, author=author)
            if user == author:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя!')
            if user.follower.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя!')
            subscription.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if not user.follower.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Вы не подписаны на этого пользователя!')
            subscription = get_object_or_404(user.follower, author=author)
            subscription.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
