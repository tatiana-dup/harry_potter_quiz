from django.db import models


class Highlights(models.TextChoices):
    DEFAULT = 'DEFAULT', 'По умолчанию'
    CORRECT = 'CORRECT', 'Верный'
    INCORRECT = 'INCORRECT', 'Неверный'