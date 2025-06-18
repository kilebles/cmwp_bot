from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import User, SurveyAnswer, UserAction
from django.contrib.auth.models import Group, User as AuthUser
import json


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'first_name', 'last_name', 'company', 'phone', 'registered_at', 'survey_completed_at')
    search_fields = ('first_name', 'last_name', 'company', 'phone', 'tg_id')
    list_filter = ('registered_at', 'survey_completed_at')


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_no', 'answer', 'created_at')
    list_filter = ('question_no', 'created_at')
    search_fields = ('answer',)


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'type')
    readonly_fields = ('formatted_payload',)
    fields = ('user', 'type', 'created_at', 'formatted_payload')

    def formatted_payload(self, obj):
        try:
            pretty = json.dumps(obj.payload, indent=2, ensure_ascii=False)
        except Exception as e:
            pretty = str(obj.payload)
        return format_html('<pre style="white-space: pre-wrap;">{}</pre>', pretty)

    formatted_payload.short_description = 'Payload (читабельно)'


admin.site.unregister(Group)
admin.site.unregister(AuthUser)
