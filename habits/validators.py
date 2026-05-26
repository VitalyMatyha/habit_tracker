from rest_framework.serializers import ValidationError


def validate_reward_and_related(reward, related_habit):
    """Нельзя одновременно указать вознаграждение и связанную привычку."""
    if reward and related_habit:
        raise ValidationError(
            "Нельзя одновременно указать вознаграждение и связанную привычку."
        )


def validate_duration(value):
    """Время выполнения не больше 120 секунд."""
    if value > 120:
        raise ValidationError(
            "Время выполнения не должно превышать 120 секунд."
        )


def validate_related_habit_is_pleasant(related_habit):
    """В связанные привычки можно добавлять только приятные привычки."""
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError(
            "Связанная привычка должна быть приятной."
        )


def validate_pleasant_habit_no_reward(is_pleasant, reward, related_habit):
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    if is_pleasant and (reward or related_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def validate_periodicity(value):
    """Периодичность не реже 1 раза в 7 дней."""
    if value > 7:
        raise ValidationError(
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
        )