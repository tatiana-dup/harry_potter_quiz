from django.db import models

from quizzes.constants import (SLUG_MAX_LENGTH,
                               TEXT_LENGTH)


class BaseNameSlugModel(models.Model):
    """Абстрактная модель, содержащая название и слаг."""
    name = models.CharField('Название', unique=True)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Part(BaseNameSlugModel):
    """Части истории, к которым могут относиться вопросы. """
    serial_number = models.PositiveSmallIntegerField('Номер части',
                                                     unique=True)

    class Meta:
        verbose_name = 'часть'
        verbose_name_plural = 'Части'
        ordering = ('serial_number',)


class Tag(BaseNameSlugModel):
    """Тэги для вопросов."""
    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)


class Question(models.Model):
    """Вопросы для квизов."""
    DIFFICULTY_CHOICES = [
        (1, 'Легкий'),
        (2, 'Средний'),
        (3, 'Сложный'),
        (4, 'Очень сложный')
    ]

    text = models.TextField('Текст вопроса')
    answer_requirements = models.TextField(
        'Требования к ответу',
        help_text='Пояснения или подсказка, каким должен быть ответ',
        null=True,
        blank=True)
    image = models.ImageField(
        'Изображение',
        help_text='Добавьте изображение, если оно нужно для вопроса.',
        upload_to='quizzes/questions/images',
        null=True,
        blank=True)
    difficulty_level = models.IntegerField(
        'Сложность',
        choices=DIFFICULTY_CHOICES,
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
        'По книгам',
        help_text='В книгах есть ответ на этот вопрос?')
    is_answer_in_movie = models.BooleanField(
        'По фильмам',
        help_text='В фильмах есть ответ на этот вопрос?')
    is_active = models.BooleanField(
        'Доступность',
        help_text='Вопрос доступен пользователю?', default=False)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('difficulty_level', 'text')

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Answer(models.Model):
    """Варианты ответов на вопросы."""
    text = models.TextField('Текст ответа')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        related_name='answers')
    is_correct = models.BooleanField('Это верный ответ?')
    description = models.TextField(
        'Пояснение',
        help_text='Можно указать, почему этот ответ является верным или нет.',
        null=True, blank=True)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_pliral = 'Ответы'
        ordering = ('text',)


class QuestionCollection(BaseNameSlugModel):
    """Коллекции вопросов по общей тематике."""
    description = models.TextField('Описание')
    questions = models.ManyToManyField(
        Question,
        verbose_name='Вопросы',
        related_name='collections'
    )
