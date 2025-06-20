import json

from django.urls import path
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from app.cmwp_bot.services.broadcast_service import send_broadcast
from .models import BroadcastMessage, StaticText, User, SurveyAnswer, UserAction
from django.contrib.auth.models import Group, User as AuthUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'tg_id', 'first_name', 'last_name', 'company', 'phone',
        'registered_at', 'survey_completed_at',
        'has_requested_plan', 'has_requested_prices', 'has_requested_discussion', 'is_admin'
    )
    search_fields = ('first_name', 'last_name', 'company', 'phone', 'tg_id')
    list_filter = ('registered_at', 'survey_completed_at', 'is_admin')

    def has_requested_plan(self, obj):
        return obj.useraction_set.filter(type='CLICK_GET_PLAN').exists()
    has_requested_plan.short_description = 'Запросил план'
    has_requested_plan.boolean = True

    def has_requested_prices(self, obj):
        return obj.useraction_set.filter(type='CLICK_PRICES').exists()
    has_requested_prices.short_description = 'Запросил стоимость'
    has_requested_prices.boolean = True

    def has_requested_discussion(self, obj):
        return obj.useraction_set.filter(type='CLICK_DISCUSS').exists()
    has_requested_discussion.short_description = 'Решил обсудить проект'
    has_requested_discussion.boolean = True

    actions = ['make_admin', 'remove_admin']

    @admin.action(description='Сделать администратором')
    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)

    @admin.action(description='Убрать права администратора')
    def remove_admin(self, request, queryset):
        queryset.update(is_admin=False)


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_no', 'answer', 'created_at')
    list_filter = ('question_no', 'created_at')
    search_fields = ('answer', 'user__first_name', 'user__last_name', 'user__phone')


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__phone', 'type')
    readonly_fields = ('formatted_payload', 'user_display', 'user_phone', 'user_company')
    fields = ('user', 'user_display', 'user_phone', 'user_company', 'type', 'created_at', 'formatted_payload')

    def formatted_payload(self, obj):
        try:
            pretty = json.dumps(obj.payload, indent=2, ensure_ascii=False)
        except Exception as e:
            pretty = str(obj.payload)
        return format_html('<pre style="white-space: pre-wrap;">{}</pre>', pretty)

    def user_display(self, obj):
        return str(obj.user)

    def user_phone(self, obj):
        return obj.user.phone or '—'

    def user_company(self, obj):
        return obj.user.company or '—'

    formatted_payload.short_description = 'Доп. информация'
    user_display.short_description = 'Пользователь'
    user_phone.short_description = 'Телефон'
    user_company.short_description = 'Компания'



@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'is_sent', 'short_text', 'send_action']
    readonly_fields = ['is_sent', 'created_at']
    fields = ['text', 'action_filter', 'is_sent', 'created_at']

    def short_text(self, obj):
        return format_html('<div style="max-width: 400px; white-space: pre-wrap;">{}</div>', obj.text[:200])
    short_text.short_description = 'Сообщение'

    def send_action(self, obj):
        if not obj.is_sent:
            return format_html('<a class="button" href="{}">Отправить</a>', f'./send/{obj.id}/')
        return 'Отправлено'
    send_action.short_description = 'Действие'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('send/<int:pk>/', self.admin_site.admin_view(self.send_broadcast_view))
        ]
        return custom + urls

    def send_broadcast_view(self, request, pk):
        message = BroadcastMessage.objects.get(pk=pk)
        if message.is_sent:
            self.message_user(request, 'Уже отправлено.', level=messages.WARNING)
        else:
            send_broadcast(message.text, action_filter=message.action_filter)
            message.is_sent = True
            message.save()
            self.message_user(request, 'Сообщение отправлено.', level=messages.SUCCESS)
        return HttpResponseRedirect("../../")
    

@admin.register(StaticText)
class StaticTextAdmin(admin.ModelAdmin):
    list_display = ['key', 'short_content', 'has_photo']
    search_fields = ['key', 'content']
    fields = ['key', 'content', 'photo_url']

    def short_content(self, obj):
        return format_html('<div style="max-width: 400px; white-space: pre-wrap;">{}</div>', obj.content[:150])

    def has_photo(self, obj):
        if obj.photo_url:
            return format_html('<a href="{}" target="_blank">📷 Ссылка</a>', obj.photo_url)
        return '—'

    short_content.short_description = 'Текст'
    has_photo.short_description = 'Фото'


admin.site.unregister(Group)
admin.site.unregister(AuthUser)
