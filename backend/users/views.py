from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from foodgram.pagination import CustomPagination
from .models import User
from .serializers import (
    UserSerializer,
    UserAvatarSerializer,
    PasswordChangeSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny,]

    def update(self, request, *args, **kwargs):
        return self.method_not_allowed(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.method_not_allowed(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="me",
    )
    def get_me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=("put", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="me/avatar",
        url_name="me/avatar",
    )
    def avatar(self, request):
        user = request.user
        if request.method == "PUT":
            serializer = UserAvatarSerializer(user, data=request.data,
                                              partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer = UserAvatarSerializer()
        serializer.delete_avatar(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
        url_path="set_password",
        url_name="set_password",
    )
    def password_change(self, request):
        serializer = PasswordChangeSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed."},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
