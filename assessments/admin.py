from django.contrib import admin
from .models import Assessment, Question, Choice, ResultInterpretation, TestResult

class ChoiceInline(admin.TabularInline):
    """Inline configuration for question answer choices."""
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    """Inline configuration for assessment questions."""
    model = Question
    extra = 1


class ResultInterpretationInline(admin.TabularInline):
    """Inline configuration for result interpretation ranges."""
    model = ResultInterpretation
    extra = 1


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    """Admin for assessment definitions and nested content."""
    list_display = ('title', 'short_name', 'questions_count', 'time_to_complete')
    prepopulated_fields = {'short_name': ('title',)}
    inlines = [ResultInterpretationInline, QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin for standalone question management."""
    list_display = ('assessment', 'order', 'text', 'scale')
    list_filter = ('assessment',)
    inlines = [ChoiceInline]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    """Read-focused admin for user test results."""
    list_display = ('user', 'assessment', 'total_score', 'created_at')
    list_filter = ('assessment', 'created_at')