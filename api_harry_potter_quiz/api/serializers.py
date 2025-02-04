from rest_framework import serializers

from api.enums import Highlights
from quizzes.models import (Answer,
                            Question,
                            QuestionCollection)


class СollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о коллекциях вопросов."""
    questions_count = serializers.SerializerMethodField()
    in_process = serializers.BooleanField(default=False)
    result = serializers.IntegerField(default=None)

    class Meta:
        model = QuestionCollection
        fields = ('id', 'slug', 'name', 'description', 'pub_date',
                  'questions_count', 'in_process', 'result',)

    def get_questions_count(self, obj):
        return obj.questions.count()


class AnswerOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения инфо о варианте ответа."""
    highlight = serializers.ChoiceField(
        choices=Highlights.choices,
        default=Highlights.DEFAULT)

    class Meta:
        model = Answer
        fields = ('id', 'text', 'highlight',)


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения инфо о вопросе."""
    question_id = serializers.IntegerField(source='id')
    options = AnswerOptionSerializer(read_only=True, many=True)
    selected_option_id = serializers.IntegerField(default=None)
    is_last_question = serializers.BooleanField(default=False)

    class Meta:
        model = Question
        fields = ('question_id', 'text', 'image', 'difficulty_level',
                  'options', 'selected_option_id', 'is_last_question',)
