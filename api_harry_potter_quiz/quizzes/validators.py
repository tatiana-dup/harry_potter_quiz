from django.core.exceptions import ValidationError

from quizzes.constants import MAX_IMAGE_SIZE_MB


def validate_image_size(file):
    if file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f'Размер файла не может превышать {MAX_IMAGE_SIZE_MB} МБ.')
