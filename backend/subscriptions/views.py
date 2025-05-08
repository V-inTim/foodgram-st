from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.pagination import DefaultPagination
from .serializers import SubscribeSerializer


class SubscriptionListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get(self, request):
        serializer = SubscribeSerializer(context={"request": request})
        subscriptions = serializer.get_subscriptions()

        paginator = self.pagination_class()
        paginated = paginator.paginate_queryset(subscriptions, request)
        return paginator.get_paginated_response(paginated)


class SubscriptionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = SubscribeSerializer(
            data={"followed_user": pk, "user": request.user.pk},
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        serializer = SubscribeSerializer(
            context={"request": request},
            data={"followed_user": pk}
        )
        if serializer.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Ошибка отписки"},
            status=status.HTTP_400_BAD_REQUEST
        )
