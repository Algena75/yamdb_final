from api_yamdb.settings import RATING_SCORE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import year_validator


class AbstractModel(models.Model):
    """Абстрактная Модель"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=False,
        blank=False
    )

    class Meta:
        abstract = True


class Genre(AbstractModel):
    """Модель Жанра."""

    def __str__(self):
        return self.name


class Category(AbstractModel):
    """Модель Категории."""

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[year_validator])
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель Жанр произведения."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        default=None
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        default=None
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_genre_title'
            )
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField(
        validators=[
            MaxValueValidator(RATING_SCORE['max']),
            MinValueValidator(RATING_SCORE['min'])
        ]
    )
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='one_review_by_title_for_user')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
