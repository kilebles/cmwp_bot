from django.contrib import admin
from .models import User, SurveyAnswer, UserAction
from django.contrib.auth.models import Group, User as AuthUser
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'phone', 'registered_at')
    search_fields = ('first_name', 'last_name', 'company', 'phone')
    list_filter = ('registered_at',)


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_number', 'question_text', 'answer_text', 'answered_at')
    list_filter = ('question_number', 'answered_at')
    search_fields = ('question_text', 'answer_text')


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__first_name', 'user__last_name', 'action')


admin.site.unregister(Group)
admin.site.unregister(AuthUser)