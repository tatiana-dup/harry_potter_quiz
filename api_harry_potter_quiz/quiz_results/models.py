from django.contrib.auth import get_user_model
from django.db import models

from quizzes.models import (Answer,
                            Question,
                            QuestionCollection)


User = get_user_model()


class UserCollectionResult(models.Model):
    """Результаты прохождения коллекций пользователем"""
    pass


class UserCollectionAttempt(models.Model):
    """Отдельная попытка прохождения коллекции пользователем."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collection_attempts',
        verbose_name='Пользователь'
    )
    collection = models.ForeignKey(
        QuestionCollection,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Коллекция вопросов'
    )
    attempt_date = models.DateTimeField('Дата прохождения', auto_now_add=True)

    class Meta:
        verbose_name = 'Попытка прохождения коллекции'
        verbose_name_plural = 'Попытки прохождения коллекций'

    def __str__(self):
        return (f"{self.user.username}, {self.collection.name}: "
                f"{self.attempt_date}")


class UserAnswer(models.Model):
    """Ответы пользователя на вопросы"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Пользователь'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name='Вопрос'
    )
    selected_answer = models.ForeignKey(
        Answer,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Выбранный ответ'
    )
    is_correct = models.BooleanField('Верный ли ответ', default=False)
    attempt = models.ForeignKey(
        UserCollectionAttempt,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Попытка'
    )

    class Meta:
        verbose_name = 'Ответ пользователя на вопрос'
        verbose_name_plural = 'Ответы пользователя на вопросы'

    def __str__(self):
        return f"{self.user.username} ответил на вопрос {self.question}"
