from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import ROLE_MAX_LENGTH


class AppUser(AbstractUser):
    """Пользователи."""

    class UserRole(models.TextChoices):
        USER = 'user', 'Пользователь'
        EDITOR = 'editor', 'Редактор'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(
        'Роль',
        max_length=ROLE_MAX_LENGTH,
        choices=UserRole.choices,
        default=UserRole.USER)
    avatar = models.ImageField(
        'Аватарка',
        upload_to='users/avatars',
        null=True,
        blank=True)
    bio = models.TextField('О себе', null=True, blank=True)

    class Meta(AbstractUser.Meta):
        ordering = ('username',)
