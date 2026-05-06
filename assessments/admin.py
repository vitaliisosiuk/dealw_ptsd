from django.contrib import admin
from .models import Assessment, Question, Choice, ResultInterpretation, TestResult

# 1. Варіанти відповідей тепер додаються до ЗАПИТАНЬ
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4 # 4 варіанти за замовчуванням ідеально для шкали Бека

# 2. Питання додаються до ТЕСТУ
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class ResultInterpretationInline(admin.TabularInline):
    model = ResultInterpretation
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_name', 'questions_count', 'time_to_complete')
    prepopulated_fields = {'short_name': ('title',)}
    inlines = [ResultInterpretationInline, QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'order', 'text', 'scale')
    list_filter = ('assessment',)
    inlines = [ChoiceInline]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'total_score', 'created_at')
    list_filter = ('assessment', 'created_at')