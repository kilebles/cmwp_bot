from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import User, SurveyAnswer, UserAction
from django.contrib.auth.models import Group, User as AuthUser
import json


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'tg_id', 'first_name', 'last_name', 'company', 'phone',
        'registered_at', 'survey_completed_at',
        'has_requested_plan', 'has_requested_discussion',
    )
    search_fields = ('first_name', 'last_name', 'company', 'phone', 'tg_id')
    list_filter = ('registered_at', 'survey_completed_at')

    def has_requested_plan(self, obj):
        return obj.useraction_set.filter(type='CLICK_GET_PLAN').exists()
    has_requested_plan.short_description = 'Запросил план'
    has_requested_plan.boolean = True

    def has_requested_discussion(self, obj):
        return obj.useraction_set.filter(type='CLICK_DISCUSS').exists()
    has_requested_discussion.short_description = 'Решил обсудить проект'
    has_requested_discussion.boolean = True


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


admin.site.unregister(Group)
admin.site.unregister(AuthUser)
