from django.contrib import admin
from .models import User, SurveyAnswer, UserAction
from django.contrib.auth.models import Group, User as AuthUser


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


admin.site.unregister(Group)
admin.site.unregister(AuthUser)
