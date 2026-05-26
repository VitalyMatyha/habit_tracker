from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from telegram_bot.bot import send_telegram_message


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках по расписанию."""
    now = timezone.localtime(timezone.now())
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        is_pleasant=False,
    ).select_related("user", "related_habit")

    for habit in habits:
        habit_time = habit.time.replace(second=0, microsecond=0)

        if habit_time == current_time:
            user = habit.user
            if not user.telegram_chat_id:
                continue

            if habit.related_habit:
                reward_text = f"Вознаграждение: {habit.related_habit.action}"
            elif habit.reward:
                reward_text = f"Вознаграждение: {habit.reward}"
            else:
                reward_text = "Без вознаграждения"

            message = (
                f"Напоминание о привычке!\n"
                f"Действие: {habit.action}\n"
                f"Место: {habit.place}\n"
                f"Время: {habit.time}\n"
                f"{reward_text}"
            )

            send_telegram_message(user.telegram_chat_id, message)