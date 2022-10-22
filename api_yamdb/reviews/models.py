from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(UserManager):
    """Для создания пользователя и суперпользователя."""

    def create_user(self, username, email, password, **extra_fields):
        return super().create_user(
            username, email=email, password=password, **extra_fields
        )

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields
        )


class User(AbstractUser):
    # пользовательские роли
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=200,
        choices=ROLES,
        default='user'
    )
    objects = MyUserManager()

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)


class Category(models.Model):
    """Категория произведения."""

    name = models.CharField(
        verbose_name='Имя категории произведения',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""

    name = models.CharField(
        verbose_name='Имя жанра произведения',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""

    name = models.CharField(
        verbose_name='Имя произведения',
        max_length=200,
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
        null=True
    )
    year = models.IntegerField(verbose_name='Год издания', )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles_m2m'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Связь Many-2-Many."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='TitleGenre_title'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='TitleGenre_genre'
    )


class Review(models.Model):
    """Отзыв на произведение."""

    text = models.TextField(verbose_name='Текст отзыва', )
    score = models.PositiveSmallIntegerField(verbose_name='Оценка', )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарий к Review."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_author'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments_review'
    )
    text = models.TextField(verbose_name='Текст комментария', )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
