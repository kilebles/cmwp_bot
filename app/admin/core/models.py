from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    company = models.CharField(max_length=255, blank=True, null=True, verbose_name='Компания')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


class SurveyAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_answers', verbose_name='Пользователь')
    question_number = models.IntegerField(verbose_name='Номер вопроса')
    question_text = models.TextField(verbose_name='Вопрос')
    answer_text = models.TextField(verbose_name='Ответ')
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')

    class Meta:
        verbose_name = 'Ответ на анкету'
        verbose_name_plural = 'Ответы на анкету'
        ordering = ['question_number']

    def __str__(self):
        return f"Ответ на вопрос {self.question_number} от {self.user}"


class UserAction(models.Model):
    ACTION_CHOICES = [
        ('get_plan', 'Получил план'),
        ('contacts', 'Запросил контакты'),
        ('how_helpful', 'Запросил обсудить проект'),
        ('email_click', 'Решил написать письмо'),
        ('telegram_click', 'Решил связаться в Telegram'),
        ('start_survey', 'Начал анкету'),
        ('complete_survey', 'Закончил анкету'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions', verbose_name='Пользователь')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name='Действие')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Когда выполнено')

    class Meta:
        verbose_name = 'Действие пользователя'
        verbose_name_plural = 'Действия пользователей'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} — {self.get_action_display()} @ {self.timestamp:%Y-%m-%d %H:%M}"
