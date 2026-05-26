from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    validate_reward_and_related,
    validate_duration,
    validate_related_habit_is_pleasant,
    validate_pleasant_habit_no_reward,
    validate_periodicity,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_duration(self, value):
        validate_duration(value)
        return value

    def validate_periodicity(self, value):
        validate_periodicity(value)
        return value

    def validate(self, data):
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant", False)

        validate_reward_and_related(reward, related_habit)
        validate_related_habit_is_pleasant(related_habit)
        validate_pleasant_habit_no_reward(is_pleasant, reward, related_habit)

        return data