from django.db import models
from .fields import SafeJSONField

ACTION_CHOICES = [
    ('REGISTRATION_FINISHED', 'Завершил регистрацию'),
    ('SURVEY_STARTED', 'Начал анкету'),
    ('SURVEY_COMPLETED', 'Завершил анкету'),
    ('CLICK_CONTACTS', 'Запросил контакты'),
    ('CLICK_GET_PLAN', 'Запросил план'),
    ('CLICK_DISCUSS', 'Решил обсудить проект'),
]


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    tg_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    first_name = models.TextField(null=True, blank=True, verbose_name='Имя')
    last_name = models.TextField(null=True, blank=True, verbose_name='Фамилия')
    company = models.TextField(null=True, blank=True, verbose_name='Компания')
    phone = models.TextField(null=True, blank=True, verbose_name='Телефон')
    registered_at = models.DateTimeField(verbose_name='Дата регистрации')
    survey_completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения анкеты')
    last_activity_at = models.DateTimeField(verbose_name='Последняя активность')

    class Meta:
        db_table = 'users'
        managed = False
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-registered_at']

    def __str__(self):
        phone_display = (
            f'+{self.phone}' if self.phone and not self.phone.startswith('+')
            else self.phone or '—'
        )
        return f'{self.first_name or ""} {self.last_name or ""} ({phone_display})'


class SurveyAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id', verbose_name='Пользователь')
    question_no = models.IntegerField(verbose_name='№ вопроса')
    answer = models.TextField(verbose_name='Ответ')
    created_at = models.DateTimeField(verbose_name='Дата ответа')

    class Meta:
        db_table = 'survey_answers'
        managed = False
        verbose_name = 'Ответ на анкету'
        verbose_name_plural = 'Ответы на анкету'
        ordering = ['user_id', 'question_no']

    def __str__(self):
        return f'Ответ {self.user} на {self.question_no}'



class UserAction(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id', verbose_name='Пользователь')
    type = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name='Тип действия')
    payload = SafeJSONField(verbose_name='Параметры', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Время')

    class Meta:
        db_table = 'user_actions'
        managed = False
        verbose_name = 'Действие пользователя'
        verbose_name_plural = 'Действия пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — {self.get_type_display()} @ {self.created_at:%Y-%m-%d %H:%M}'