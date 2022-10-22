from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics
from django.conf import settings

from api.serializers import (
    ConformationCodeSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    TitleSerializer
)
from reviews.models import User, Category, Genre, Title, Review
from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    IsAuthorOrAdministratorOrReadOnly
)
from .mixins import BaseModelViewSet


class APISignUp(generics.CreateAPIView):
    """Регистрация пользователя."""

    # регестрация доступна всем
    permission_classes = (AllowAny,)

    def post(self, request):
        """Пользователь отправил email и usernameна эндпоинт .../signup/."""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        # Берем пользователя, который только, что был создан
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        # создаем confirmation_code
        confirmation_code = default_token_generator.make_token(user)
        # отправляем email
        # https://docs.djangoproject.com/en/4.0/topics/email/
        send_mail(
            subject='Код подтверждения вашего email',
            message=f'{confirmation_code}',
            from_email=settings.EMAIL_HOST,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(
            {'email': serializer.data['email'],
             'username': serializer.data['username']},
            status=status.HTTP_200_OK
        )


class APIToken(generics.CreateAPIView):
    """Выдача токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Обработка POST-запрос с username и confirmation_code."""
        serializer = ConformationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # если данные валидны, то в таком случае проверяем, есть ли
        # пользователь.
        user = get_object_or_404(
            User, username=serializer.data['username']
        )
        # если пользователь существуют, то проверим его confirmation_code
        if default_token_generator.check_token(
                user, serializer.data['confirmation_code']
        ):
            # Теперь можно выслать токен для доступа пользователю
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation code': 'Код подтверждения не верен!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class APIUser(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(BaseModelViewSet):
    """Работа с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseModelViewSet):
    """Работа с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Работа с моделью произведений."""

    queryset = Title.objects.all()
    serializer_class = ReadOnlyTitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Работа с отзывами пользователей."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Работа с комментариями пользователей."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments_review.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
