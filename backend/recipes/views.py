from rest_framework import status, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import DefaultPagination
from api.permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipeSerializer,
    ShoppingListSerializer,
    FavoriteSerializer,
)
from .models import Recipe
from .filters import RecipeFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=("get",),
        permission_classes=(AllowAny,),
        url_path="get-link",
        url_name="get-link",
    )
    def get_link(self, request, pk):
        instance = self.get_object()

        url = f"{request.get_host()}/s/{instance.id}"

        return Response(data={"short-link": url})

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="download_shopping_cart",
        url_name="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        serializer = ShoppingListSerializer(
            context={"request": request},
        )
        content = serializer.get_shopping_list()
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="shopping_cart",
        url_name="shopping_cart",
    )
    def shopping_cart(self, request, pk=None):
        if request.method == "POST":
            serializer = ShoppingListSerializer(
                data={"recipe": pk, "user": request.user.pk},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = ShoppingListSerializer(
            context={"request": request},
            data={"recipe": pk}
        )
        if serializer.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Рецепт не найден в списке покупок."},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="favorite",
        url_name="favorite",
    )
    def favorite(self, request, pk=None):
        if request.method == "POST":
            serializer = FavoriteSerializer(
                data={"recipe": pk, "user": request.user.pk},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = FavoriteSerializer(
            context={"request": request},
            data={"recipe": pk}
        )
        if serializer.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Рецепт не найден в избранном."},
            status=status.HTTP_400_BAD_REQUEST
        )
