from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


class SurveyAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_answers')
    question_number = models.IntegerField()
    question_text = models.TextField()
    answer_text = models.TextField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question_number']


class UserAction(models.Model):
    ACTION_CHOICES = [
        ('get_plan', 'Получить план'),
        ('contacts', 'Контакты'),
        ('how_helpful', 'Обсудить мой проект'),
        ('email_click', 'Написать письмо'),
        ('telegram_click', 'Связаться в Telegram'),
        ('start_survey', 'Начал анкету'),
        ('complete_survey', 'Закончил анкету'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.get_action_display()} @ {self.timestamp:%Y-%m-%d %H:%M}"
