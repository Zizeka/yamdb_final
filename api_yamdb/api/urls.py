from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APISignUp, APIToken, APIUser, CategoryViewSet,
                    CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register('users', APIUser, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')

urls_v1_auth = [
    # Пользователь отправляет POST-запрос на добавление нового пользователя
    # с параметрами email и username в ответ conformation_code
    path('signup/', APISignUp.as_view(), name='signup'),
    # Пользователь отправляет POST-запрос с параметрами username и
    # confirmation_code на эндпоин в ответ токен
    path('token/', APIToken.as_view(), name='token'),
]

urlpatterns = [
    # При желании пользователь отправляет PATCH-запрос на эндпоинт и заполняет
    # поля в своём профайле (описание полей — в документации).
    # path('v1/users/me/', APIUser.as_view(), name='me'),
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urls_v1_auth))
]
