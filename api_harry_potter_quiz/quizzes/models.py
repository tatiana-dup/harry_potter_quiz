from django.db import models

from quizzes.constants import SLUG_MAX_LENGTH


class Part(models.Model):
    name = models.CharField('Название', unique=True)
    serial_number = models.PositiveSmallIntegerField('Номер части',
                                                     unique=True)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'часть'
        verbose_name_plural = 'Части'
        ordering = ('serial_number',)


class Tag(models.Model):
    name = models.CharField('Название', unique=True)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Легкий'),
        (2, 'Средний'),
        (3, 'Сложный'),
        (4, 'Очень сложный')
    ]

    text = models.TextField('Текст вопроса')
    answer_requirements = models.TextField(
        'Пояснение, каким должен быть ответ', null=True, blank=True)
    image = models.ImageField('Изображение',
                              upload_to='quizzes/questions/images')
    difficulty_level = models.IntegerField(choices=DIFFICULTY_CHOICES,
                                           default=1)
