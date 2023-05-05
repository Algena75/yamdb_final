from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Код для авторизации',
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True)
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True)

    role = models.CharField(
        max_length=30,
        choices=ROLES_CHOICES,
        default='user',
        verbose_name='Роль пользователя'
    )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR or self.is_staff

    def __str__(self) -> str:
        return self.username
