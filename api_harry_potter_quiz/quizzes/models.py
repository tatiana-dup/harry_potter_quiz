from django.db import models

from quizzes.constants import (SLUG_MAX_LENGTH,
                               TEXT_LENGTH)


class BaseNameSlugModel(models.Model):
    name = models.CharField('Название', unique=True)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)


class Part(BaseNameSlugModel):
    serial_number = models.PositiveSmallIntegerField('Номер части',
                                                     unique=True)

    class Meta:
        verbose_name = 'часть'
        verbose_name_plural = 'Части'
        ordering = ('serial_number',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Tag(BaseNameSlugModel):

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


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
    part = models.ForeignKey(
        Part,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Часть',
        related_name='questions')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='questions')
    is_answer_in_book = models.BooleanField(
        'В книге есть ответ на этот вопрос?')
    is_answer_in_movie = models.BooleanField(
        'В фильме есть ответ на этот вопрос?')
    is_active = models.BooleanField(
        'Доступен пользователю?', default=False)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('difficulty_level', 'text')

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Answer(models.Model):
    text = models.TextField('Текст ответа')
    description = models.TextField('Пояснение', null=True, blank=True)
    is_correct = models.BooleanField('Это верный ответ?')

    class Meta:
        verbose_name = 'ответ'
        verbose_name_pliral = 'Ответы'
        ordering = ('text',)


class QuestionCollection(models.Model):
    pass
