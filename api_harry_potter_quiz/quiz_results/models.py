from django.db import models


class UserCollectionResult(models.Model):
    """Результаты прохождения коллекций пользователем"""
    pass


class UserCollectionAttempt(models.Model):
    """Отдельная попытка прохождения коллекции пользователем."""
    pass


class UserAnswer(models.Model):
    """Ответы пользователя на вопросы"""
    pass
