from django.db import models
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дней)",
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
    )
    duration = models.PositiveIntegerField(
        verbose_name="Время на выполнение (сек)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user} — {self.action} в {self.time}"