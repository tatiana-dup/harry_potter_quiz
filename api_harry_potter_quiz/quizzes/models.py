from django.db import models

from quizzes.constants import (NAME_MAX_LENGTH,
                               SLUG_MAX_LENGTH,
                               LIMIT_STRING_DISPLAYED)
from quizzes.validators import validate_image_size


class BaseNameSlugModel(models.Model):
    """Абстрактная модель, содержащая название и слаг."""
    name = models.CharField(
        'Название', max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(
        'Слаг', max_length=SLUG_MAX_LENGTH, unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:LIMIT_STRING_DISPLAYED]


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

    class Difficulty(models.IntegerChoices):
        EASY = 1, 'Легкий'
        MEDIUM = 2, 'Средний'
        HARD = 3, 'Сложный'
        EXTRA_HARD = 4, 'Очень сложный'

    text = models.TextField('Текст вопроса')
    answer_requirements = models.TextField(
        'Требования к ответу',
        help_text='Пояснения или подсказка, каким должен быть ответ',
        null=True,
        blank=True)
    image = models.ImageField(
        'Изображение',
        help_text='При необходимости вы можете добавить изображение до 3 МБ.',
        upload_to='quizzes/questions/images',
        null=True,
        blank=True,
        validators=[validate_image_size])
    difficulty_level = models.IntegerField(
        'Сложность',
        choices=Difficulty.choices,
        default=Difficulty.EASY)
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
        help_text='Вопрос доступен пользователю?',
        default=True)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('difficulty_level', 'text')

    def __str__(self):
        return self.text[:LIMIT_STRING_DISPLAYED]


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
        verbose_name_plural = 'Ответы'
        ordering = ('text',)


class QuestionCollection(BaseNameSlugModel):
    """Коллекции вопросов по конкретной тематике."""
    description = models.TextField('Описание')
    questions = models.ManyToManyField(
        Question,
        verbose_name='Вопросы',
        related_name='collections'
    )
    is_active = models.BooleanField(
        'Доступность',
        help_text='Коллекция доступна пользователю?',
        default=False)
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True)
    pub_date = models.DateTimeField(
        'Дата публикации',
        help_text=('Установить дату, когда коллекция должна быть'
                   'опубликована.'))

    class Meta:
        verbose_name = 'коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ('-pub_date',)
